import maya.cmds as cmds
import leg_rig
import custom_controls
class create_arm_rig:
    def __init__(self):
        self.l = leg_rig.create_rig()

    def make_arm_rig(self, side, clavicle, shoulder, elbow, wrist, color):
        #variables
        if not cmds.objExists('joints'):
            cmds.group(em=True, n='joints')
            cmds.group(em=True, n='controls')
            cmds.group(em=True, n='IKs')
        else:
            pass
        self.controls = []

        # disconnect shoulder joint
        cmds.disconnectJoint(shoulder)
        new_joint = cmds.pickWalk(clavicle, d='down')
        clavicle_end = cmds.rename(new_joint, clavicle + '_end')

        cmds.disconnectJoint(wrist)
        new_joint = cmds.pickWalk(elbow, d='down')
        elbow_end = cmds.rename(new_joint, elbow + '_end')

        # duplicate arm
        cmds.duplicate(shoulder, n='shoulder_' + side + '_ik')
        cmds.duplicate(shoulder, n='shoulder_' + side + '_fk')

        # variables for fk chain
        fk_shoulder = 'shoulder_' + side + '_fk'
        temp = cmds.pickWalk(fk_shoulder, d='down')
        fk_elbow = cmds.rename(temp, 'elbow_' + side + '_fk')
        temp = cmds.pickWalk(fk_elbow, d='down')
        fk_elbow_end = cmds.rename(temp, 'elbow_' + side + '_end_fk')
        cmds.parent(fk_shoulder, clavicle_end)


        # variables for ik chain
        ik_shoulder = 'shoulder_' + side + '_ik'
        temp = cmds.pickWalk(ik_shoulder, d='down')
        ik_elbow = cmds.rename(temp, 'elbow_' + side + '_ik')
        temp = cmds.pickWalk(ik_elbow, d='down')
        ik_elbow_end = cmds.rename(temp, 'elbow_' + side + '_end_ik')

        # create ik_fk_switch control
        legs = leg_rig.create_rig()
        legs.create_ik_fk_switch(side, 'wrist_' + side + '_bind', 'arm', color, 0,0,-5, [0,1,0])
        cmds.matchTransform('ik_fk_arm_' + side + '_Grp', wrist)
        self.ik_fk_control = 'ik_fk_arm_' + side

        cmds.parent(wrist, elbow_end)
        #create ik fk chains
        self.make_fk_joint_chain(fk_shoulder, fk_elbow, wrist, color)
        cmds.parent(fk_shoulder, w =True)
        self.make_ik_joint_chain(side, ik_shoulder, ik_elbow, ik_elbow_end, wrist, color)

        # create ikfk switch
        self.ik_fk_switch(fk_shoulder, ik_shoulder, shoulder)
        self.ik_fk_switch(fk_elbow, ik_elbow, elbow)

        # make clavicle controls
        self.make_clavicle_controls(clavicle, side, color)
        cmds.parentConstraint(cmds.pickWalk(clavicle, d = 'down'), ik_shoulder)

        # parent everything to groups
        cmds.parent(fk_shoulder, ik_shoulder, shoulder, 'joints')
        self.l.stretchy(ik_shoulder, wrist, 'arm_stretchy_curve_' + side, side, shoulder, elbow, self.stretchy_joint, self.ik_fk_control)

    def make_clavicle_controls(self, clavicle, side, color):
        obj_control = cmds.circle(n = 'clavicle_' + side + '_Ctl', nr = [1,0,0], r = 5)
        cmds.setAttr(obj_control[0] + '.lineWidth', 2)
        self.l.override_colors(obj_control[0], color)
        obj_control_null = cmds.group(n= obj_control[0] + '_Null')
        cmds.parent(obj_control_null, 'controls')
        cmds.matchTransform(obj_control_null, clavicle, pos=True, rot=True)
        cmds.parentConstraint(obj_control, clavicle)

        parent_obj = cmds.pickWalk(clavicle, direction='up')
        if parent_obj[0] == clavicle:
            pass
        else:
            cmds.parentConstraint(parent_obj, obj_control_null, mo=True)

    def ik_fk_switch(self, ik_joint, fk_joint, main_joint):
        cmds.pairBlend(nd = main_joint, at = ['tx','ty', 'tz'])
        pair_blend = cmds.rename('pairBlend1', main_joint + '_pairblend')
        cmds.connectAttr(pair_blend + '.outRotate', main_joint + '.r')
        cmds.connectAttr(pair_blend + '.outTranslate', main_joint + '.t')

        cmds.connectAttr(ik_joint + '.t',pair_blend + '.inTranslate2')
        cmds.connectAttr(ik_joint + '.r',pair_blend + '.inRotate2')

        cmds.connectAttr(fk_joint + '.t',pair_blend + '.inTranslate1')
        cmds.connectAttr(fk_joint + '.r',pair_blend + '.inRotate1')

        #connect control to ikfk
        cmds.connectAttr(self.ik_fk_control + '.ikfk', pair_blend + '.weight')

    def make_fk_joint_chain(self, fk_shoulder, fk_elbow, wrist, color):
        fk_joints = [fk_shoulder, fk_elbow, wrist]

        # create fk chain
        for obj in fk_joints:
            obj_control = cmds.circle(n=obj + '_Ctl', nr = [1,0,0], r = 5)
            cmds.setAttr(obj_control[0] + '.lineWidth', 2)
            self.l.override_colors(obj_control[0], color)
            obj_control_group = cmds.group(obj_control, n=obj + '_Ctl_Null')
            cmds.matchTransform(obj_control_group, obj, pos=True, rot=True)
            cmds.orientConstraint(obj_control, obj)
            cmds.parent(obj_control_group, 'controls')
            try:
                parent_obj= cmds.pickWalk(obj, direction='up')
                if parent_obj[0] ==obj:
                    pass
                else:
                    cmds.parentConstraint(parent_obj, obj_control_group, mo=True)
            except:
                pass
            #hide controls if its ik mode
            condition = cmds.shadingNode('condition', asUtility=True, n='condition_node' + obj_control[0])
            cmds.connectAttr(self.ik_fk_control + '.ikfk', condition + '.firstTerm')
            cmds.connectAttr(condition + '.outColorR', obj_control[0] + '.visibility')
            self.controls.append(obj_control_group)

    def make_ik_joint_chain(self, side, shoulder, knee, elbow_end, wrist, color):
        # make ik handle and control
        cmds.ikHandle(n='ik_arm_' + side, sj = shoulder, ee = elbow_end, sol = 'ikRPsolver')
        ik_arm = 'ik_arm_' + side
        cmds.parent(ik_arm, 'IKs')
        c = custom_controls.create_custom_controls()
        arm_control = c.cube_curve('ANIM_arm_' + side)
        cmds.setAttr(arm_control + '.lineWidth', 2)
        self.l.override_colors(arm_control, color)
        cmds.xform(arm_control, cp=True)
        arm_control_grp = cmds.group(arm_control, n = 'grp_ANIM_arm_' + side)
        cmds.matchTransform(arm_control_grp, elbow_end, pos=True, rot = True)
        self.controls.append(arm_control_grp)
        cmds.parent(arm_control_grp, 'controls')
        cmds.parentConstraint(arm_control, 'ik_arm_' + side)

        #create a pole vector
        pv = self.l.create_pole_vector(side, shoulder, knee, elbow_end, 'arm', 'ik_arm_' + side, color)
        orient_constraint_wrist = cmds.orientConstraint(arm_control, wrist)[0]
        cmds.setDrivenKeyframe(orient_constraint_wrist + '.' + wrist + '_Ctl' + 'W0', cd = self.ik_fk_control + '.ikfk', v=0, dv=0)
        cmds.setDrivenKeyframe(orient_constraint_wrist + '.' + wrist + '_Ctl' + 'W0', cd = self.ik_fk_control + '.ikfk', v=1, dv=1)

        cmds.setDrivenKeyframe(orient_constraint_wrist + '.ANIM_arm_' + side + 'W1', cd = self.ik_fk_control + '.ikfk', v=1, dv=0)
        cmds.setDrivenKeyframe(orient_constraint_wrist + '.ANIM_arm_' + side + 'W1', cd = self.ik_fk_control + '.ikfk', v=0, dv=1)

        #hide visiblity
        condition = cmds.shadingNode('condition', asUtility=True, n='condition_node' + arm_control)
        cmds.connectAttr(self.ik_fk_control + '.ikfk', condition + '.firstTerm')
        cmds.connectAttr(condition + '.outColorR', arm_control + '.visibility')
        cmds.connectAttr(condition + '.outColorR', pv + '.visibility')

        cmds.setAttr(condition + '.colorIfTrueR', 1)
        cmds.setAttr(condition + '.colorIfFalseR', 0)

        #make a joint for stretching
        self.stretchy_joint = cmds.joint()
        cmds.setAttr(self.stretchy_joint + '.drawStyle', 2)
        cmds.matchTransform(self.stretchy_joint, arm_control)
        cmds.parent(self.stretchy_joint, arm_control)

arm_rig = create_arm_rig()
