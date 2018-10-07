import maya.cmds as cmds
import maya.api.OpenMaya as om
import custom_controls

class create_rig:
    def create_leg_rig(self, side, root, thigh, knee, ankle, foot, foot_end, heel, color):
        #variables
        self.controls = []

        # disconnect ankle joint
        cmds.disconnectJoint(ankle)
        new_joint = cmds.pickWalk(knee, d='down')
        cmds.rename(new_joint, knee + '_end')

        # duplicate thigh
        cmds.duplicate(thigh, n='thigh_' + side + '_ik')
        cmds.duplicate(thigh, n='thigh_' + side + '_fk')

        # variables for fk chain
        fk_thigh = 'thigh_' + side + '_fk'

        temp = cmds.pickWalk(fk_thigh, d='down')
        fk_knee = cmds.rename(temp, 'shin_' + side + '_fk')

        temp = cmds.pickWalk(fk_knee, d='down')
        fk_knee_end = cmds.rename(temp, 'knee_end_' + side + '_fk')

        fk_knee_end_control = 'knee_end_' + side + '_fk_Ctl'

        # variables for ik chain
        ik_thigh = 'thigh_' + side + '_ik'

        temp = cmds.pickWalk(ik_thigh, d='down')
        ik_knee = cmds.rename(temp, 'shin_' + side + '_ik')

        temp = cmds.pickWalk(ik_knee, d='down')
        ik_knee_end = cmds.rename(temp, 'knee_end_' + side + '_ik')

        # cmds.pointConstraint(ik_knee_end, ankle, mo=True)

        #create ik_fk_switch control
        self.create_ik_fk_switch(side, ankle, 'leg', color, 5,0,0, [0,0,1])
        self.controls.append(self.ik_fk_control)

        #create ik fk chains
        self.make_ik_joint_chain(side, ik_thigh, ik_knee, ik_knee_end, ankle, foot, foot_end, heel, color)
        self.make_fk_joint_chain(fk_thigh, fk_knee, fk_knee_end, ankle, fk_knee_end_control, color)

        cmds.matchTransform(self.ik_fk_control_grp, 'ik_leg_' + side)

        #make ik fk switch
        self.ik_fk_switch(ik_thigh, fk_thigh, thigh)
        self.ik_fk_switch(ik_knee, fk_knee, knee)

        try:
            if cmds.pickWalk(root, d = 'up') == root:
                cmds.parent(root, 'joints')
            else:
                pass
        except ValueError:
            pass

        cmds.parent(ankle, 'joints')
        self.ankle_switch(ankle, side)

        #toe fk
        self.make_fk_control([foot], color)
        constraint = cmds.listRelatives(foot, ad=True, type='orientConstraint')[0]
        self.toe_ik_fk_switch(foot, constraint)

        #make leg stretchy
        self.stretchy(ik_thigh, ankle, 'leg_stretchy_curve_' + side, side, thigh, knee, self.stretchy_joint, self.ik_fk_control)

    def override_colors(self, obj, color):
        cmds.setAttr(obj + '.overrideEnabled', 1)
        cmds.setAttr(obj + '.overrideRGBColors', 1)
        cmds.setAttr(obj + '.overrideColorRGB', color[0], color[1], color[2])

    def create_ik_fk_switch(self, side, parent, name, color, m1, m2, m3, normal):
        self.ik_fk_control = cmds.circle(n='ik_fk_' + name + '_' + side, nr = normal)[0]
        self.override_colors(self.ik_fk_control, color)
        cmds.move(m1, m2, m3, self.ik_fk_control + '.scalePivot', self.ik_fk_control + '.rotatePivot')
        self.ik_fk_control_grp = cmds.group(self.ik_fk_control, n = 'ik_fk_' + name + '_' + side +'_Grp' )
        cmds.move(m1, m2, m3, self.ik_fk_control_grp + '.scalePivot', self.ik_fk_control_grp + '.rotatePivot')
        cmds.parent(self.ik_fk_control_grp, parent)
        cmds.select(self.ik_fk_control)
        cmds.addAttr(shortName='ikfk', longName='ik_fk_switch', at = 'double', min = 0, max =1, defaultValue=0, k=True)
        cmds.addAttr(shortName='stretch', longName='stretch', at = 'double', min = 0, max = 1, defaultValue=0, k=True)

        #delete unnecessary attributes
        cmds.setAttr('ik_fk_' + name + '_' + side + '.tx', lock = True, keyable = False, channelBox = False)
        cmds.setAttr('ik_fk_' + name + '_' + side + '.ty', lock = True, keyable = False, channelBox = False)
        cmds.setAttr('ik_fk_' + name + '_' + side + '.tz', lock = True, keyable = False, channelBox = False)
        cmds.setAttr('ik_fk_' + name + '_' + side + '.rx', lock = True, keyable = False, channelBox = False)
        cmds.setAttr('ik_fk_' + name + '_' + side + '.ry', lock = True, keyable = False, channelBox = False)
        cmds.setAttr('ik_fk_' + name + '_' + side + '.rz', lock = True, keyable = False, channelBox = False)
        cmds.setAttr('ik_fk_' + name + '_' + side + '.sx', lock = True, keyable = False, channelBox = False)
        cmds.setAttr('ik_fk_' + name + '_' + side + '.sy', lock = True, keyable = False, channelBox = False)
        cmds.setAttr('ik_fk_' + name + '_' + side + '.sz', lock = True, keyable = False, channelBox = False)
        cmds.setAttr('ik_fk_' + name + '_' + side + '.visibility', lock = True, keyable = False, channelBox = False)

    def make_fk_control(self, joints, color):
        # create fk chain
        for obj in joints:
            obj_control = cmds.circle(n = obj + '_Ctl', nr = [1,0,0], r = 5)
            cmds.setAttr(obj_control[0] + '.lineWidth', 2)
            self.override_colors(obj_control[0], color)
            obj_control_group = cmds.group(obj_control, n = obj + '_Ctl_Null')
            cmds.matchTransform(obj_control_group, obj, pos=True, rot=True)
            cmds.orientConstraint(obj_control, obj)
            cmds.parent(obj_control_group, 'controls')
            parentOBJ = cmds.pickWalk(obj, direction='up')
            if parentOBJ[0] ==obj:
                pass
            else:
                cmds.parentConstraint(parentOBJ, obj_control_group, mo=True)

            #hide controls if its ik mode
            condition = cmds.shadingNode('condition', asUtility=True, n='condition_node' + obj_control[0])
            cmds.connectAttr(self.ik_fk_control + '.ikfk', condition + '.firstTerm')
            cmds.connectAttr(condition + '.outColorR', obj_control[0] + '.visibility')
            self.controls.append(obj_control_group)

    def make_fk_joint_chain(self, fk_thigh, fk_knee, fk_knee_end, ankle, fk_knee_end_control, color):
        fk_joints = [fk_thigh, fk_knee, fk_knee_end]
        self. make_fk_control(fk_joints, color)

        constraint = cmds.listRelatives(fk_knee_end, ad = True, type = 'parentConstraint')
        cmds.delete(constraint)

        cmds.pointConstraint(fk_knee_end_control, ankle, mo = 1)
        cmds.orientConstraint(fk_knee_end_control, ankle, mo = 1)

    def make_ik_joint_chain(self, side, thigh, knee, knee_end, ankle, toe, toe_end, heel, color):
        # make ik handle and control
        ik_leg = cmds.ikHandle(n='ik_leg_' + side, sj = thigh, ee = knee_end, sol = 'ikRPsolver')
        c = custom_controls.create_custom_controls()
        self.leg_control = c.cube_curve('ANIM_leg_' + side)
        self.override_colors(self.leg_control, color)
        cmds.setAttr(self.leg_control + '.lineWidth', 2)
        cmds.xform(self.leg_control, cp=True)
        self.leg_control_grp = cmds.group(self.leg_control, n = 'grp_ANIM_leg_' + side)
        cmds.matchTransform(self.leg_control_grp, ik_leg, pos=True)
        self.controls.append(self.leg_control_grp)
        cmds.parent(self.leg_control_grp, 'controls')

        #create a pole vector
        self.create_pole_vector(side, thigh, knee, knee_end, 'leg', 'ik_leg_' + side, color)

        #create toe roll joint
        jDrv_foot = cmds.duplicate(toe, name = 'jDrv_bind_foot_' + side)
        temp = cmds.pickWalk(jDrv_foot[0], d='down')
        cmds.delete(temp)
        cmds.parent(jDrv_foot, toe)

        # creating locators
        #
        loc_ankle = cmds.spaceLocator(n='locDrv_ankle_' + side)[0]
        loc_ankle_grp = cmds.group(loc_ankle, n='locDrv_ankle_' + side + '_Null')
        cmds.matchTransform(loc_ankle_grp, ankle)

        ##
        loc_toe_grp = cmds.duplicate(loc_ankle_grp, n = 'locDrv_foot_' + side + '_Null')[0]
        temp = cmds.pickWalk(loc_toe_grp, d = 'down')
        loc_toe = cmds.rename(temp, 'locDrv_foot_' + side)
        cmds.matchTransform(loc_toe_grp, toe, pos = True)
        cmds.matchTransform(loc_toe_grp, ankle, rot = True)

        ###
        loc_toe_end_grp = cmds.duplicate(loc_toe_grp, n = 'locDrv_toe_' + side + '_Null')[0]
        temp = cmds.pickWalk(loc_toe_end_grp, d = 'down')
        loc_toe_end = cmds.rename(temp, 'locDrv_toe_' + side)
        cmds.matchTransform(loc_toe_end_grp, toe_end)

        ####
        loc_heel = cmds.spaceLocator(n='locDrv_heel_' + side)[0]
        loc_heel_grp = cmds.group(loc_heel, n='locDrv_heel_' + side + '_Null')
        cmds.matchTransform(loc_heel_grp, heel)

        ##parenting
        cmds.parent(loc_ankle, loc_toe)
        cmds.parent(loc_toe_grp, loc_toe_end)
        cmds.parent(loc_toe_end_grp, loc_heel)
        cmds.delete(loc_ankle_grp)
        cmds.parent(loc_heel_grp, self.leg_control)

        ##constraints
        cmds.pointConstraint(loc_ankle, 'ik_leg_' + side)
        cmds.orientConstraint(loc_toe, ankle, mo = True)
        cmds.orientConstraint(loc_toe_end, toe, mo = True)

        #creating controls for foot system
        toe_Ctl = cmds.curve(n = 'ANIM_toe_' + side, d = 1, p =[(-1,0,-1), (1,0,-1), (1,0,1),(-1,0,1),(-1,0,-1)], k = [0,1,2,3,4] )
        toe_end_Ctl = cmds.curve(n = 'ANIM_toe_end_' + side, d =1, p=[ (0, 1, 1), (0, 1, -1), (0, -1, -1), (0,-1, 1), (0, 1, 1) ], k = [0,1,2,3,4])
        heel_Ctl = cmds.curve(n = 'ANIM_heel_' + side, d =1, p=[ (-1, 1, 0), (1, 1, 0), (1, -1, 0), (-1,-1, 0), (-1, 1, 0) ], k = [0,1,2,3,4])

        self.controls.extend((toe_Ctl, toe_end_Ctl, heel_Ctl))
        self.foot_controls = [toe_Ctl, toe_end_Ctl, heel_Ctl]

        grp_foot_controls = self.group_foot_controls(self.foot_controls)
        grp_grp_foot_controls = self.group_foot_controls(grp_foot_controls)

        cmds.parent('ANIM_heel_' + side + '_grp_grp', loc_heel_grp)
        cmds.parent('ANIM_toe_' + side + '_grp_grp', loc_toe_grp)
        cmds.parent('ANIM_toe_end_' + side + '_grp_grp', loc_toe_end_grp)
        self.alignObjs(grp_grp_foot_controls)

        # orientConstraint
        cmds.orientConstraint(toe_Ctl, loc_toe, mo = True)
        cmds.orientConstraint(heel_Ctl, loc_heel)
        cmds.orientConstraint(toe_end_Ctl, loc_toe_end)

        # create an attribute for toe roll and foot roll
        cmds.select(self.leg_control)
        cmds.addAttr(shortName='tr', longName='toe_roll', defaultValue=0, k=True)
        cmds.addAttr(shortName='fr', longName='foot_roll', defaultValue=0, minValue=-10, maxValue=10, k=True)
        cmds.connectAttr(self.leg_control + '.toe_roll', jDrv_foot[0] + '.rz')

        cmds.setDrivenKeyframe('ANIM_toe_end_' + side + '_grp.rz', cd=self.leg_control + '.fr', v=0, dv=0)
        cmds.setDrivenKeyframe('ANIM_toe_' + side + '_grp.rz', cd=self.leg_control + '.fr', v=0, dv=0)
        cmds.setDrivenKeyframe('ANIM_heel_' + side + '_grp.rx', cd=self.leg_control + '.fr', v=0, dv=0)

        cmds.setDrivenKeyframe('ANIM_toe_end_' + side + '_grp.rz', cd = self.leg_control + '.fr', v = 0, dv=4)
        cmds.setDrivenKeyframe('ANIM_toe_' + side + '_grp.rz', cd = self.leg_control + '.fr', v=-45, dv=5)
        cmds.setDrivenKeyframe('ANIM_toe_end_' + side + '_grp.rz', cd = self.leg_control + '.fr', v=-70, dv=10)
        cmds.setDrivenKeyframe('ANIM_toe_' + side + '_grp.rz', cd = self.leg_control + '.fr', v=40, dv=10)

        cmds.setDrivenKeyframe('ANIM_toe_end_' + side + '_grp.rz', cd = self.leg_control + '.fr', v=0, dv=-10)
        cmds.setDrivenKeyframe('ANIM_toe_' + side + '_grp.rz', cd = self.leg_control + '.fr', v=-0, dv=-10)
        cmds.setDrivenKeyframe('ANIM_heel_' + side + '_grp.rx', cd = self.leg_control + '.fr', v=-40, dv=-10)

        # hide locators
        self.hideShape([loc_toe_end, loc_toe, loc_heel, loc_ankle])
        cmds.parent('ik_leg_' + side, 'IKs')

        condition = cmds.shadingNode('condition', asUtility=True, n='condition_node' + self.leg_control_grp[0])
        cmds.setAttr(condition + '.secondTerm', 1)
        cmds.connectAttr(self.ik_fk_control + '.ikfk', condition + '.firstTerm')
        cmds.connectAttr(condition + '.outColorR', self.leg_control_grp + '.visibility')
        cmds.connectAttr(condition + '.outColorR', 'PV_ik_leg_' + side + '_Null' + '.visibility')

        for obj in self.foot_controls:
            cmds.connectAttr(condition + '.outColorR', obj + '.visibility')

        #point Constraint ankle
        cmds.pointConstraint('ik_leg_' + side, ankle, mo=True)
        cmds.pointConstraint(knee_end, ankle, mo=True)

        #make a joint for stretching
        self.stretchy_joint = cmds.joint()
        cmds.setAttr(self.stretchy_joint + '.drawStyle', 2)
        cmds.matchTransform(self.stretchy_joint, self.leg_control)
        cmds.parent(self.stretchy_joint, self.leg_control)

    def create_pole_vector(self,side, thigh, knee, knee_end, name, ik, color):
        #create a pole vector
        start = cmds.xform(thigh, ws = True, q = True,  t = True)
        mid = cmds.xform(knee, ws = True, q = True,  t = True)
        end = cmds.xform(knee_end, ws = True, q = True,  t = True)
        startV = om.MVector(start[0], start[1], start[2])
        midV = om.MVector(mid[0], mid[1], mid[2])
        endV = om.MVector(end[0], end[1], end[2])

        start_point = endV - startV
        mid_point = midV - startV

        dotP = mid_point * start_point
        proj = float(dotP) / float(start_point.length())

        start_point_N = start_point.normal()
        projV = start_point_N * proj

        arrowV = (mid_point - projV)*30
        arrowV *= 0.5
        finalV = arrowV + midV

        c = custom_controls.create_custom_controls()
        control = c.knee_curve('PV_ik_' + name + '_' + side)
        self.override_colors(control, color)
        control_group = cmds.group(control, n = 'PV_ik_' + name + '_' + side + '_Null')
        cmds.xform(control_group, ws=1, t=(finalV.x, finalV.y, finalV.z))
        cmds.parent(control_group, 'controls')

        #pole vector constraint locator to ik
        cmds.poleVectorConstraint(control, ik)
        return control

    def ik_fk_switch(self, ik_joint, fk_joint, main_joint):
        cmds.pairBlend(nd = main_joint, at = ['tx','ty', 'tz'])
        pair_blend = cmds.rename('pairBlend1', main_joint + '_pairblend')
        cmds.connectAttr(pair_blend + '.outRotate', main_joint + '.r')
        cmds.connectAttr(pair_blend + '.outTranslate', main_joint + '.t')

        cmds.connectAttr(ik_joint + '.t',pair_blend + '.inTranslate1')
        cmds.connectAttr(ik_joint + '.r',pair_blend + '.inRotate1')

        cmds.connectAttr(fk_joint + '.t',pair_blend + '.inTranslate2')
        cmds.connectAttr(fk_joint + '.r',pair_blend + '.inRotate2')

        #connect control to ikfk
        cmds.connectAttr(self.ik_fk_control + '.ikfk', pair_blend + '.weight')

    def ankle_switch(self, ankle, side):
        point = cmds.listRelatives(ankle, ad = True, type = 'pointConstraint')
        orient = cmds.listRelatives(ankle, ad = True, type = 'orientConstraint')

        #make pairBlend
        pairBlend = cmds.shadingNode('pairBlend', asUtility=True, n='pairBlend_' + ankle)
        cmds.connectAttr(self.ik_fk_control + '.ikfk', pairBlend + '.weight')
        cmds.setAttr(pairBlend + '.inTranslateX1', 1)
        cmds.setAttr(pairBlend + '.inTranslateY2', 1)


        ######
        pc_attr = cmds.listAttr(point)
        condition_pc = cmds.shadingNode('condition', asUtility=True, n = 'pc_ankle_' + side + '_condition')
        cmds.connectAttr(self.ik_fk_control + '.stretch', condition_pc + '.firstTerm')
        cmds.setAttr(condition_pc + '.secondTerm', 0)
        cmds.setAttr(condition_pc + '.operation', 1)

        cmds.setAttr(condition_pc + '.colorIfTrueR', 0)
        cmds.setAttr(condition_pc + '.colorIfFalseR', 1)

        cmds.setAttr(condition_pc + '.colorIfTrueG', 1)
        cmds.setAttr(condition_pc + '.colorIfFalseG', 0)

        #condition for ikfk all tothere three constraints
        condition_ik_fk = cmds.shadingNode('condition', asUtility=True, n='pc_ankle_' + side + '_condition_ik_fk')
        cmds.connectAttr(self.ik_fk_control + '.ikfk', condition_ik_fk + '.firstTerm')
        cmds.connectAttr(condition_pc + '.outColorR', condition_ik_fk + '.colorIfTrueR')
        cmds.connectAttr(condition_pc + '.outColorG', condition_ik_fk + '.colorIfTrueG')

        cmds.setAttr(condition_ik_fk + '.colorIfFalseR', 0)
        cmds.setAttr(condition_ik_fk + '.colorIfFalseG', 0)

        cmds.connectAttr(condition_ik_fk + '.outColorG', point[0] + '.' + pc_attr[-3])
        cmds.connectAttr(condition_ik_fk + '.outColorR', point[0] + '.' + pc_attr[-2])

        #condition for FK
        condition_fk = cmds.shadingNode('condition', asUtility=True, n='pc_ankle_' + side + '_condition_fk')
        cmds.connectAttr(self.ik_fk_control + '.ikfk', condition_fk + '.firstTerm')
        cmds.connectAttr(condition_fk + '.outColorR', point[0] + '.' + pc_attr[-1])

        for obj in orient:
            try:
                cmds.connectAttr(pairBlend + '.outTranslateX', obj + '.locDrv_foot_' + side + 'W0')
                cmds.connectAttr(pairBlend + '.outTranslateY', obj + '.knee_end_' + side + '_fk_CtlW1')
            except RuntimeError:
                pass

    def toe_ik_fk_switch(self, object, constraint):
        reverse = cmds.shadingNode('reverse', asUtility=True, n='reverse_' + object)
        attr = cmds.listAttr(constraint)
        cmds.connectAttr(self.ik_fk_control + '.ikfk', constraint + '.' + attr[-1])
        cmds.connectAttr(self.ik_fk_control + '.ikfk', reverse + '.inputX')
        cmds.connectAttr(reverse + '.outputX', constraint + '.' + attr[-2])

    def hideShape(self, objects):
        for obj in objects:
            cmds.setAttr(obj + "Shape.visibility", 0)

    def group_foot_controls(self, controls):
        groupObjs = []
        for obj in controls:
            emptyGroup = groupObjs.append(cmds.group(em=True, n=str(obj) + "_grp"))
            cmds.parent(obj, emptyGroup)
        return groupObjs

    def alignObjs(self, objs):
        for obj in objs:
            cmds.xform(obj, t = (0,0,0), ro = (0,0,0))

    def stretchy(self, obj_start, obj_end, name, side, scale_obj_first, scale_obj_second, stretchy_joint, ik_fk_control):
        obj_start_pos = cmds.xform(obj_start, t = True, ws = True, q = True)
        obj_end_pos = cmds.xform(obj_end, t = True, ws = True, q = True)

        stretchy_curve = cmds.curve(d=1, p=[obj_start_pos, obj_end_pos], k = (0, 1), n = name)
        cmds.parent(stretchy_curve, 'extra')
        cmds.skinCluster(obj_start, stretchy_joint, stretchy_curve, tsb=True)

        shape = cmds.listRelatives(stretchy_curve)[0]
        curve_info_node = cmds.shadingNode('curveInfo', asUtility=True, n = stretchy_curve + '_' + 'side_curve_info')
        MD_node = cmds.shadingNode('multiplyDivide', asUtility=True, n = stretchy_curve + '_' + side + '_MD')
        condition_node = cmds.shadingNode('condition', asUtility=True, n = stretchy_curve + '_' + side + '_condition')

        cmds.connectAttr(shape + '.worldSpace[0]', curve_info_node + '.inputCurve')
        cmds.connectAttr(curve_info_node + '.arcLength', MD_node + '.input1X')
        arc_length = cmds.getAttr(curve_info_node + '.arcLength')
        cmds.setAttr(MD_node + '.input2X', arc_length)
        cmds.setAttr(MD_node + '.operation', 2)

        cmds.connectAttr(curve_info_node + '.arcLength', condition_node + '.firstTerm')
        cmds.setAttr(condition_node + '.secondTerm', arc_length)
        cmds.setAttr(condition_node + '.operation', 4)
        cmds.setAttr(condition_node + '.colorIfTrueR', 1)

        #glooal scale
        global_scale_MD = cmds.shadingNode('multiplyDivide', asUtility=True, n = 'global_scale_MD')
        cmds.setAttr(global_scale_MD + '.operation', 2)
        cmds.connectAttr(MD_node + '.outputX', global_scale_MD + '.input1X')
        cmds.connectAttr('main_control.sx', global_scale_MD + '.input2X')
        cmds.connectAttr(global_scale_MD + '.outputX', condition_node + '.colorIfFalseR')

        # connect condition node for fk mode as well
        condition_fk = cmds.shadingNode('condition', asUtility=True, n = stretchy_curve + '_' + side + '_condition_fk')
        cmds.connectAttr(ik_fk_control + '.ikfk', condition_fk + '.firstTerm')
        cmds.setAttr(condition_fk + '.secondTerm', 0)
        cmds.setAttr(condition_fk + '.operation', 0)

        cmds.connectAttr(condition_node + '.outColorR', condition_fk + '.colorIfTrueR')
        cmds.setAttr(condition_fk + '.colorIfFalseR', 1)

        # set another condition node for stretch on and off
        condition_stretch = cmds.shadingNode('condition', asUtility=True, n = stretchy_curve + '_' + side + 'condition_stretch')
        cmds.connectAttr(ik_fk_control + '.stretch', condition_stretch + '.firstTerm')
        cmds.setAttr(condition_stretch + '.secondTerm', 0)
        cmds.setAttr(condition_stretch + '.operation', 1)

        cmds.connectAttr(condition_fk + '.outColorR', condition_stretch + '.colorIfTrueR')
        cmds.setAttr(condition_stretch + '.colorIfFalseR', 1)

        cmds.connectAttr(condition_stretch + '.outColorR', scale_obj_first + '.sx')
        cmds.connectAttr(condition_stretch + '.outColorR', scale_obj_second + '.sx')

        # volume preservation
        MD_volume_node = cmds.shadingNode('multiplyDivide', asUtility=True, n = "MD_volume_" + side)
        cmds.connectAttr(condition_stretch + '.outColorR', MD_volume_node + '.input1Y')
        cmds.connectAttr(condition_stretch + '.outColorR', MD_volume_node + '.input2Y')

        MD_volume_node_2 = cmds.shadingNode('multiplyDivide', asUtility=True, n = "MD_volume_" + side)
        cmds.setAttr(MD_volume_node_2 + '.input1Y', 1)
        cmds.setAttr(MD_volume_node_2 + '.operation', 2)
        cmds.connectAttr(MD_volume_node + '.outputY', MD_volume_node_2 + '.input2Y')

        cmds.connectAttr(MD_volume_node_2 + '.outputY', scale_obj_first + '.sy')
        cmds.connectAttr(MD_volume_node_2 + '.outputY', scale_obj_first + '.sz')
        cmds.connectAttr(MD_volume_node_2 + '.outputY', scale_obj_second + '.sy')
        cmds.connectAttr(MD_volume_node_2 + '.outputY', scale_obj_second + '.sz')

leg_rig = create_rig()



