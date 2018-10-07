import maya.cmds as cmds
import custom_controls
import leg_rig

class create_spine_rig:

    def __init__(self):
        self.c_controls = custom_controls.create_custom_controls()
        self.l = leg_rig.create_rig()

    def make_spine_rig(self, root, chest, neck, neck2, head, color):
        ribbon_spine_joint_group = []

        source_joint = root
        child_joint = chest
        child_joint_tx = cmds.getAttr(child_joint + ".tx")
        source_joint_rad = cmds.getAttr(source_joint + ".radius")
        source_joint_pos = cmds.xform(source_joint, t = True, q = True, ws = True)
        child_joint_pos = cmds.xform(child_joint, t = True, q = True, ws = True)

        #'For' loop - set joint quantity
        ribbon_spine_joints = []
        chest_joints_poss = []
        chest_joints_poss.append(source_joint_pos)

        #create additional root joint
        cmds.select(source_joint)
        start_jnt = cmds.joint(n = 'hip_joint_bind', o = [0, 0, 0])
        ribbon_spine_joints.append(start_jnt)
        cmds.select(root)

        count = 1
        while (count<5):
            #Create joints and match their orientation to source joint
            joint_added = cmds.joint(n = 'chest_bind_0' + str(count), r = source_joint_rad,  o = [0, 0, 0])
            ribbon_spine_joints.append(joint_added)

            #Set distance for new joints
            cmds.xform(joint_added, t=((child_joint_tx/5), 0, 0))
            joint_position = cmds.xform(joint_added, t=True, q=True, ws=True)
            chest_joints_poss.append(joint_position)
            cmds.select(joint_added)
            count = count + 1
        chest_joints_poss.append(child_joint_pos)
        cmds.parent(chest, w = True)

        for obj in ribbon_spine_joints:
            cmds.parent(obj, w = True)

            #create control
            control = cmds.circle(n = obj + '_Ctl', nr = [1,0,0], r = 7)
            self.l.override_colors(control[0], color)
            cmds.setAttr(control[0] + '.lineWidth', 2)
            control_Null = cmds.group(control, n = control[0] + '_Null')
            control_group = cmds.group(control_Null, n = control[0] + '_Grp')
            cmds.connectAttr('main_control.scale', control_group + '.scale')
            cmds.parent(control_group, 'extra')
            locator = cmds.spaceLocator(n = obj + '_loc')
            cmds.matchTransform(locator, obj)
            cmds.parent(locator[0], control_group)
            cmds.xform(locator, t=(0, 20, 0))
            cmds.matchTransform(control_group, obj)
            cmds.parent(obj, control[0])
            ribbon_spine_joint_group.append(control_group)
            cmds.setAttr(locator[0] + '.visibility', 0)

        ribbon_spine_joints.append(chest)
        for id, obj in enumerate(ribbon_spine_joints):
            temp = cmds.pickWalk(obj, d = 'up')
            constrained_obj = cmds.pickWalk(temp, d = 'up')
            try:
                cmds.aimConstraint(ribbon_spine_joints[id+1], constrained_obj, worldUpType = 'object', worldUpObject = obj + '_loc')
            except IndexError:
                pass

        ribbon_curve_l = cmds.curve(d=3, p=[chest_joints_poss[0], chest_joints_poss[1], chest_joints_poss[2], chest_joints_poss[3],
                            chest_joints_poss[4], chest_joints_poss[5]], k = (0, 0, 0, 1, 2, 3, 3, 3), n = 'ribbon_curve')

        ribbon_curve_r = cmds.duplicate(ribbon_curve_l)

        cmds.xform(ribbon_curve_l, t = (2,0,0), ws = True)
        cmds.xform(ribbon_curve_r, t = (-2,0,0), ws = True)
        cmds.loft(ribbon_curve_l, ribbon_curve_r, d = 3, ch=True, rn=True, ar=True, n= 'ribbon_surface')
        ribbon_surface = 'ribbon_surface'
        cmds.delete(ribbon_curve_l, ribbon_curve_r)

        #conect ribbon to joints
        cmds.select(d = True)
        chest_mid_joint = cmds.joint(n = 'chest_mid', r = source_joint_rad*2,  o = [90, 0, 90])
        xpos = (chest_joints_poss[3][0]+chest_joints_poss[2][0])/2
        ypos = (chest_joints_poss[3][1]+chest_joints_poss[2][1])/2
        zpos = (chest_joints_poss[3][2]+chest_joints_poss[2][2])/2
        cmds.xform(chest_mid_joint, t=(xpos, ypos, zpos), ws = 1)
        cmds.skinCluster(root, chest, chest_mid_joint, ribbon_surface, tsb=True)

        #create controls for ribbon spine joints
        root_control = self.c_controls.cube_curve('root_Ctl')
        cmds.setAttr(root_control + '.lineWidth', 2)
        chest_control = cmds.circle(n = 'chest_Ctl', nr = [1,0,0], r = 10)[0]
        cmds.setAttr(chest_control + '.lineWidth', 2)
        back_control = cmds.circle(n = 'back_control', nr = [1,0,0], r = 10)[0]
        cmds.setAttr(back_control + '.lineWidth', 2)

        self.l.override_colors(root_control, [0,0.7,0])
        self.l.override_colors(chest_control, [0,0.7,0])
        self.l.override_colors(back_control, [0,0.7,0])

        #parent joints under controls except for root
        root_group = cmds.group(root_control, n = root + '_Null')
        cmds.matchTransform(root_group, root)
        self.create_parent_control(chest_control, chest)
        self.create_parent_control(back_control, chest_mid_joint)

        chest_group = cmds.pickWalk(chest_control, d = 'up')
        back_group = cmds.pickWalk(back_control, d = 'up')

        cmds.parentConstraint(root_control, chest_group, mo = True)
        spine_group = cmds.group(em = True)
        cmds.matchTransform(spine_group, root_control)
        cmds.parentConstraint(spine_group, back_group, mo = True)
        cmds.parentConstraint(chest_control, back_group, mo = True)

        cmds.parent(spine_group, root_control)
        for obj in ribbon_spine_joint_group:
            self.attach_joint_to_surface(ribbon_surface, obj)
            cmds.normalConstraint(ribbon_surface, obj, aimVector = (0,-1,0), upVector = (1,0,0))

        #work on root control
        start_jnt_control = cmds.pickWalk(start_jnt, d = 'up')
        start_jnt_control_grp = cmds.pickWalk(start_jnt_control, d = 'up')
        hip_gr = cmds.group(n = start_jnt_control[0] + '_extra_Null', empty = True)
        cmds.connectAttr('main_control.scale', hip_gr + '.scale')
        cmds.matchTransform(hip_gr, start_jnt_control)
        cmds.parent(start_jnt_control, hip_gr)

        cmds.parent(start_jnt, start_jnt_control_grp)
        cmds.parentConstraint(root_control, hip_gr, mo = True)
        cmds.parentConstraint(start_jnt_control, root, mo = True)

        #create controls for neck and back
        neck_joints = [neck, neck2, head]
        # create fk chain
        for obj in neck_joints:
            obj_control = cmds.circle(n=obj + '_Ctl', nr = [1,0,0], r = 7)
            # cmds.setAttr(obj_control[0] + '.lineWidth', 2)
            self.l.override_colors(obj_control[0], [0, 0.7, 0.7])
            obj_control_group = cmds.group(obj_control, n = obj + '_Ctl_Null')
            cmds.matchTransform(obj_control_group, obj, pos=True, rot=True)
            cmds.parentConstraint(obj_control, obj)
            cmds.parent(obj_control_group, 'controls')
            try:
                parentOBJ = cmds.pickWalk(obj, direction='up')
                cmds.parentConstraint(parentOBJ, obj_control_group, mo=True)
            except:
                pass
        cmds.setAttr(ribbon_surface + '.visibility', 0)

        #parent everything to groups
        cmds.parent(back_group, chest_group, root_group, 'controls')
        cmds.parent(ribbon_surface, hip_gr,  'extra')
        cmds.parent(chest_mid_joint, chest, root, 'joints')

    def create_parent_control(self, control, joint):
        #create controls for ribbon spine joints
        control_group = cmds.group(control, n = control + '_Null')
        cmds.matchTransform(control_group, joint)
        cmds.parentConstraint(control, joint)

    def attach_joint_to_surface(self, surface, joint):
        clo_po_on_sur = cmds.shadingNode('closestPointOnSurface', asShader=True, n='temp')
        cmds.connectAttr(surface + '.worldSpace[0]', clo_po_on_sur + '.inputSurface')
        cmds.connectAttr(joint + '.translate', clo_po_on_sur + '.inPosition')
        V = cmds.getAttr(clo_po_on_sur + '.result.parameterV')
        U = cmds.getAttr(clo_po_on_sur + '.result.parameterU')
        cmds.delete(clo_po_on_sur)

        po_on_sur_inf = cmds.shadingNode('pointOnSurfaceInfo', asShader=True, n = joint + '_pointOnSurfaceInfo')
        cmds.connectAttr(surface + '.worldSpace[0]', po_on_sur_inf + '.inputSurface')
        cmds.setAttr(po_on_sur_inf + '.parameterU', U)
        cmds.setAttr(po_on_sur_inf + '.parameterV', V)
        cmds.connectAttr(po_on_sur_inf + '.result.position', joint + '.translate')

spine_rig = create_spine_rig()

