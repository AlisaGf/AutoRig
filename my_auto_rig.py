from PySide2 import QtCore, QtGui, QtUiTools, QtWidgets
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
import maya.cmds as cmds
import leg_rig
import arm_rig
import spine_rig
import leg_rig

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QMainWindow)

class auto_rig_ui(QtWidgets.QDockWidget):
    if cmds.window('auto_rig_window', exists=True):
        cmds.deleteUI('auto_rig_window')

    def __init__(self, parent=maya_main_window()):

        if cmds.window('auto_rig_window', exists=True):
            cmds.deleteUI('auto_rig_window')

        super(auto_rig_ui, self).__init__(parent)
        self.setWindowTitle('Auto Rig UI')
        self.setObjectName('auto_rig_window')
        self.setFloating(True)
        self.setWidget(QtWidgets.QWidget())

        # UI
        vbox = QtWidgets.QVBoxLayout()
        self.widget().setLayout(vbox)

        # label
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        self.label = QtWidgets.QLabel('Create Skeleton')
        hbox.addWidget(self.label)

        # create skeleton button
        hbox_2 = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox_2)
        self.button_create_skeleton = QtWidgets.QPushButton('Create Skeleton')
        self.button_create_skeleton.setMinimumWidth(100)
        self.button_create_skeleton.setMaximumWidth(100)
        self.button_create_skeleton.setMinimumHeight(30)
        self.button_create_skeleton.setMaximumHeight(30)
        hbox_2.addWidget(self.button_create_skeleton)

        # create check boxes
        vbox_2 = QtWidgets.QVBoxLayout()
        hbox_2.addLayout(vbox_2)
        hbox_3 = QtWidgets.QHBoxLayout()
        vbox_2.addLayout(hbox_3)
        hbox_4 = QtWidgets.QHBoxLayout()

        vbox_2.addLayout(hbox_4)
        hbox_5 = QtWidgets.QHBoxLayout()
        vbox_2.addLayout(hbox_5)
        self.checkBox_spheres_leg = QtWidgets.QCheckBox("Leg")
        self.checkBox_spheres_spine = QtWidgets.QCheckBox("Spine")
        self.checkBox_spheres_arm = QtWidgets.QCheckBox("Arm      ")
        self.checkBox_spheres_fingers = QtWidgets.QCheckBox("Fingers")
        self.spacer = QtWidgets.QLabel("")
        self.checkBox_spheres_select_all = QtWidgets.QCheckBox("Select All")

        hbox_3.addWidget(self.checkBox_spheres_leg)
        hbox_3.addWidget(self.checkBox_spheres_spine)
        hbox_4.addWidget(self.checkBox_spheres_arm)
        hbox_4.addWidget(self.checkBox_spheres_fingers)
        hbox_5.addWidget(self.spacer)
        hbox_5.addWidget(self.checkBox_spheres_select_all)

        self.checkBox_spheres_select_all.setCheckState(QtCore.Qt.Checked)
        self.checkBox_spheres_leg.setCheckState(QtCore.Qt.Checked)
        self.checkBox_spheres_spine.setCheckState(QtCore.Qt.Checked)
        self.checkBox_spheres_arm.setCheckState(QtCore.Qt.Checked)
        self.checkBox_spheres_fingers.setCheckState(QtCore.Qt.Checked)

        # line 1
        hbox_line_1 = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox_line_1)
        self.line_1 = QtWidgets.QFrame()
        self.line_1.setLineWidth(1)
        self.line_1.setMidLineWidth(1)
        self.line_1.setFrameShape(self.line_1.HLine)
        self.line_1.setFrameShadow(self.line_1.Sunken)
        hbox_line_1.addWidget(self.line_1)

        # joint radius label
        hbox_6 = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox_6)
        self.joint_radius_label = QtWidgets.QLabel('Joint Radius')
        hbox_6.addWidget(self.joint_radius_label)

        # joint radius slider and spinbox
        hbox_7 = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox_7)

        self.joints_radius_slider = QtWidgets.QSlider()
        self.joints_radius_slider.setOrientation(QtCore.Qt.Horizontal)
        hbox_7.addWidget(self.joints_radius_slider)

        self.joints_radius_spinBox = QtWidgets.QSpinBox()
        hbox_7.addWidget(self.joints_radius_spinBox)

        # delete skeleton button
        hbox_8 = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox_8)
        self.button_delete_skeleton = QtWidgets.QPushButton('Delete Skeleton')
        hbox_8.addWidget(self.button_delete_skeleton)

        # make separation line
        hbox_line_2 = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox_line_2)
        self.line_2 = QtWidgets.QFrame()
        self.line_2.setLineWidth(1)
        self.line_2.setMidLineWidth(1)
        self.line_2.setFrameShape(self.line_2.HLine)
        self.line_2.setFrameShadow(self.line_2.Sunken)
        hbox_line_2.addWidget(self.line_2)

        #Control rig label
        hbox_label = QtWidgets.QLabel("Control Rig")
        vbox.addWidget(hbox_label)

        # create skeleton buttons
        hbox_9 = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox_9)
        self.create_control_rig_button = QtWidgets.QPushButton('Create Control Rig')
        self.select_bind_joints_button = QtWidgets.QPushButton('Select Bind Joints')
        self.create_control_rig_button.setMinimumWidth(100)
        self.create_control_rig_button.setMaximumWidth(100)
        self.create_control_rig_button.setMinimumHeight(30)
        self.create_control_rig_button.setMaximumHeight(30)

        self.select_bind_joints_button.setMinimumWidth(100)
        self.select_bind_joints_button.setMaximumWidth(100)
        self.select_bind_joints_button.setMinimumHeight(30)
        self.select_bind_joints_button.setMaximumHeight(30)

        hbox_9.addWidget(self.create_control_rig_button)
        hbox_9.addWidget(self.select_bind_joints_button)

        # close button
        hbox_10 = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox_10)
        self.close_button = QtWidgets.QPushButton('Close')
        hbox_10.addWidget(self.close_button)

        #slider
        self.updateFromSpinbox = False

        # placeholders
        self.joints = {}
        self.dict = {}
        self.spheres = []
        self.polyplanes = []
        self.control_radius = []

        # connect GUI
        self.connect_GUI()
        self.l = leg_rig.create_rig()

    def connect_GUI(self):
        self.button_create_skeleton.clicked.connect(self.create_skeleton)
        self.button_delete_skeleton.clicked.connect(self.delete_skeleton)

        # disable all if select all is disabled
        self.checkBox_spheres_select_all.stateChanged.connect(self.selectAllCheckChanged)

        # make sliders to depend on spinbox
        self.joints_radius_slider.valueChanged[int].connect(self.update_joints_radius_spinbox)
        self.joints_radius_spinBox.editingFinished.connect(self.update_joint_radius_slider_position)
        self.joints_radius_slider.setValue(1)

        # create controls rig
        self.create_control_rig_button.clicked.connect(self.create_control_rig)

        # select all bind joints
        self.select_bind_joints_button.clicked.connect(self.select_bind_joints)

        # close
        self.close_button.clicked.connect(self.closeIt)

    def closeIt(self):
        self.close()

    #for joints radius
    def update_joints_radius_spinbox(self, value):
        if not self.updateFromSpinbox:
            self.joints_radius_spinBox.setValue(value)
            self.myFunction_joints_radius()

        joints = cmds.ls(type = 'joint')
        for obj in (joints):
            cmds.setAttr(obj + '.radius', self.joints_radius_slider.value())

    def update_joint_radius_slider_position(self):
        self.updateFromSpinbox = True
        self.joints_radius_slider.setSliderPosition(self.joints_radius_spinBox.value())
        self.updateFromSpinbox = False
        self.myFunction_joints_radius()

    def myFunction_joints_radius(self):
        self.joints_radius_slider.value()

    def update_controls_radius_slider_position(self):
        self.updateFromSpinbox = True
        self.controls_radius_slider.setSliderPosition(self.controls_radius_spinBox.value())
        self.updateFromSpinbox = False
        self.myFunction_joints_radius()

    def myFunction_controls_radius(self):
        self.controls_radius_slider.value()

    def delete_skeleton(self):
        try:
            cmds.delete('*_bind') #maybe rename joint and give them something like autoR prefix
        except:
            print 'no joints to delete'

    def select_bind_joints(self):
        try:
            sel = cmds.ls('*_bind*', type = 'joint')
            cmds.select(sel)
        except ValueError:
            print 'No joints found in the scene.'

    def selectAllCheckChanged(self):
        if not self.checkBox_spheres_select_all.isChecked():
            self.checkBox_spheres_leg.setCheckState(QtCore.Qt.Unchecked)
            self.checkBox_spheres_spine.setCheckState(QtCore.Qt.Unchecked)
            self.checkBox_spheres_arm.setCheckState(QtCore.Qt.Unchecked)
            self.checkBox_spheres_fingers.setCheckState(QtCore.Qt.Unchecked)
        else:
            self.checkBox_spheres_leg.setCheckState(QtCore.Qt.Checked)
            self.checkBox_spheres_spine.setCheckState(QtCore.Qt.Checked)
            self.checkBox_spheres_arm.setCheckState(QtCore.Qt.Checked)
            self.checkBox_spheres_fingers.setCheckState(QtCore.Qt.Checked)

    def make_joint(self, joint_name, body_part, radius, n1,n2,n3):
        joint = cmds.joint(n = joint_name, r = radius,  o=[0, 0, 0])
        cmds.xform(joint, ws = True, t= (n1, n2, n3))
        cmds.select(d = True)

        if self.joints.has_key(body_part):
            self.joints[body_part].append(joint)
        else:
            self.joints.update({body_part : [joint]})

    def create_leg_joints(self):
        self.make_joint('thigh_l_bind','leg_joints', 2, 5, 81,-3)
        self.make_joint('shin_l_bind', 'leg_joints', 1, 5, 43, -2.5)
        self.make_joint('ankle_l_bind', 'leg_joints', 2, 5, 6.3, -3.6)
        self.make_joint('foot_l_driven', 'leg_joints', 2, 5.8, 1.5, 7.4)
        self.make_joint('foot_l_end', 'leg_joints', 1, 5.8, 0, 12.3)
        self.make_joint('heel_l_bind', 'leg_joints',1, 4.8, 0, -6.6)

    def create_spine_joints(self):
        self.make_joint('root_bind', 'spine_joints', 2.5, 0, 83, -2.6)
        self.make_joint('chest_bind', 'spine_joints', 2, 0, 110, -2.8)
        self.make_joint('neck_bind', 'spine_joints', 1, 0, 117.5, -3)
        self.make_joint('neck_02_bind', 'spine_joints', 1, 0, 125, -3)
        self.make_joint('head_bind', 'spine_joints', 2, 0, 136, -3)
        self.make_joint('head_end', 'spine_joints', 1, 0, 150, -3)

    def create_arm_joints(self):
        self.make_joint('clavicle_l_bind', 'arm_joints', 1, 2.5, 110, -2.8)
        self.make_joint('shoulder_l_bind', 'arm_joints', 2, 8.3, 113, -2.8)
        self.make_joint('elbow_l_bind', 'arm_joints', 2, 26.2, 96.3, -2.3)
        self.make_joint('wrist_l_bind', 'arm_joints', 2, 41.3, 82.2, -0.1)
        self.make_joint('wrist_l_end', 'arm_joints', 1, 53.2, 70.2, 1.6)

    def create_finger_joints(self):
        self.make_joint('thumb_base_l_bind', 'thumb_joints', 0.5, 42.8, 79.6, 2.2)
        self.make_joint('thumb_mid_l_bind', 'thumb_joints', 0.5, 43.6, 77.6, 3.7)
        self.make_joint('thumb_end_l_bind', 'thumb_joints', 0.5, 44.2, 75.8, 5.1)
        self.make_joint('thumb_l_last', 'thumb_joints', 0.5, 45, 73.5, 7)

        self.make_joint('index_base_l_bind','index_joints', 0.5, 46.6, 77.1, 2.4)
        self.make_joint('index_mid_l_bind', 'index_joints', 0.5, 48.7, 74.5, 3.1)
        self.make_joint('index_end_l_bind', 'index_joints', 0.5, 49.8, 73, 3.5)
        self.make_joint('index_l_last', 'index_joints', 0.5, 51, 71.5, 4)

        self.make_joint('middle_base_l_bind', 'middle_joints', 0.5, 46.3, 76.5, 0.8)
        self.make_joint('middle_mid_l_bind', 'middle_joints', 0.5, 49.6, 73.5, 1.2)
        self.make_joint('middle_end_l_bind', 'middle_joints', 0.5, 51, 72, 1.5)
        self.make_joint('middle_l_last', 'middle_joints', 0.5, 53, 70.2, 1.8)

        self.make_joint('ring_base_l_bind', 'ring_joints', 0.5, 46.3, 76.5, -0.8)
        self.make_joint('ring_mid_l_bind', 'ring_joints', 0.5, 49, 73.2, -0.6)
        self.make_joint('ring_end_l_bind', 'ring_joints', 0.5, 50.1, 71.7, -0.4)
        self.make_joint('ring_l_last', 'ring_joints', 0.5, 51.9, 70, -0.3)

        self.make_joint('pinky_base_l_bind', 'pinky_joints', 0.5, 45.7, 76.1, -2)
        self.make_joint('pinky_mid_l_bind', 'pinky_joints', 0.5, 47.4, 73.8, -2)
        self.make_joint('pinky_end_l_bind', 'pinky_joints', 0.5, 48.4, 72.4, -2.2)
        self.make_joint('pinky_l_last','pinky_joints',  0.5, 49.5, 71.1, -2.4)

    def create_skeleton(self):

        # create leg joints
        if self.checkBox_spheres_leg.isChecked():
            if not cmds.objExists('thigh_l_bind'):
                self.create_leg_joints()

        # create arm joints
        if self.checkBox_spheres_arm.isChecked():
            if not cmds.objExists('clavicle_l_bind'):
                self.create_arm_joints()

        # create spine joints
        if self.checkBox_spheres_spine.isChecked():
            if not cmds.objExists('root_l_bind'):
                self.create_spine_joints()

        # create finger joints
        if self.checkBox_spheres_fingers.isChecked():
            if not cmds.objExists('thumb_l_bind'):
                self.create_finger_joints()

        self.parent_joints_to_each_other()

    def reorient_joints(self):
        # reorient LEGS
        if cmds.objExists('thigh_l_bind'):
            #orient joints
            cmds.joint('thigh_l_bind', e =True, children = True, oj = 'xyz', secondaryAxisOrient = 'yup')
            self.orient_mid_joint('thigh_l_bind', 'shin_l_bind', 'ankle_l_bind')
            cmds.setAttr('foot_l_end.jointOrientX', 0)
            cmds.setAttr('foot_l_end.jointOrientY', 0)
            cmds.setAttr('foot_l_end.jointOrientZ', 0)
        else:
            pass

        # reorient arms
        if cmds.objExists('clavicle_l_bind'):
            cmds.joint('clavicle_l_bind', e =True, children = True, oj = 'xyz', secondaryAxisOrient = 'yup')
        else:
            pass

        # reorient fingers
        if cmds.objExists('thumb_l_bind'):
            cmds.joint('thumb_base_l_bind', e =True, children = True, oj = 'xyz', secondaryAxisOrient = 'yup')
            cmds.joint('index_base_l_bind', e =True, children = True, oj = 'xyz', secondaryAxisOrient = 'yup')
            cmds.joint('middle_base_l_bind', e =True, children = True, oj = 'xyz', secondaryAxisOrient = 'yup')
            cmds.joint('ring_base_l_bind', e =True, children = True, oj = 'xyz', secondaryAxisOrient = 'yup')
            cmds.joint('pinky_base_l_bind', e =True, children = True, oj = 'xyz', secondaryAxisOrient = 'yup')

        else:
            pass

        # orient spine
        if cmds.objExists('root_l_bind'):
            cmds.joint('root_bind', e=True, children=True, oj='xyz', secondaryAxisOrient='yup')
        else:
            pass

    def parent_joints_to_each_other(self):
        #parent and orient LEGS
        if cmds.objExists('thigh_l_bind'):
            try:
                self.joints['leg_joints'].reverse()
                for idx, item in enumerate(self.joints['leg_joints']):
                    if idx + 1 < len(self.joints['leg_joints']):
                        cmds.parent(item, self.joints['leg_joints'][idx + 1])
                    else:
                        break
                cmds.parent('heel_l_bind', 'ankle_l_bind')

                # orient joints
                cmds.joint('thigh_l_bind', e=True, children=True, oj='xyz', secondaryAxisOrient='yup')
                self.orient_mid_joint('thigh_l_bind', 'shin_l_bind', 'ankle_l_bind')
                cmds.setAttr('foot_l_end.jointOrientX', 0)
                cmds.setAttr('foot_l_end.jointOrientY', 0)
                cmds.setAttr('foot_l_end.jointOrientZ', 0)

            except KeyError:
                pass

        else:
            pass

        # parent and orient ARMS
        if cmds.objExists('clavicle_l_bind'):
            try:
                self.joints['arm_joints'].reverse()

                for idx, item in enumerate(self.joints['arm_joints']):
                    if idx+1 < len(self.joints['arm_joints']):
                        cmds.parent(item, self.joints['arm_joints'][idx + 1])
                    else:
                        break

                cmds.joint('clavicle_l_bind', e=True, children=True, oj='xyz', secondaryAxisOrient='yup')
            except KeyError:
                pass

        # parent and orient fingers
        if cmds.objExists('thumb_base_l_bind'):
            try:
                self.joints['thumb_joints'].reverse()
                self.joints['index_joints'].reverse()
                self.joints['middle_joints'].reverse()
                self.joints['ring_joints'].reverse()
                self.joints['pinky_joints'].reverse()

                for idx, item in enumerate(self.joints['thumb_joints']):
                    if idx+1 < len(self.joints['thumb_joints']):
                        cmds.parent(item, self.joints['thumb_joints'][idx + 1])
                    else:
                        break

                for idx, item in enumerate(self.joints['index_joints']):
                    if idx+1 < len(self.joints['index_joints']):
                        cmds.parent(item, self.joints['index_joints'][idx + 1])
                    else:
                        break

                for idx, item in enumerate(self.joints['middle_joints']):
                    if idx+1 < len(self.joints['middle_joints']):
                        cmds.parent(item, self.joints['middle_joints'][idx + 1])
                    else:
                        break

                for idx, item in enumerate(self.joints['ring_joints']):
                    if idx+1 < len(self.joints['ring_joints']):
                        cmds.parent(item, self.joints['ring_joints'][idx + 1])
                    else:
                        break
                for idx, item in enumerate(self.joints['pinky_joints']):
                    if idx+1 < len(self.joints['pinky_joints']):
                        cmds.parent(item, self.joints['pinky_joints'][idx + 1])
                    else:
                        break

                cmds.joint('thumb_base_l_bind', e=True, children=True, oj='xyz', secondaryAxisOrient='yup')
                cmds.joint('index_base_l_bind', e=True, children=True, oj='xyz', secondaryAxisOrient='yup')
                cmds.joint('middle_base_l_bind', e=True, children=True, oj='xyz', secondaryAxisOrient='yup')
                cmds.joint('ring_base_l_bind', e=True, children=True, oj='xyz', secondaryAxisOrient='yup')
                cmds.joint('pinky_base_l_bind', e=True, children=True, oj='xyz', secondaryAxisOrient='yup')
            except KeyError:
                pass


        # parent and orient SPINE
        if cmds.objExists('root_bind'):
            try:
                self.joints['spine_joints'].reverse()

                for idx, item in enumerate(self.joints['spine_joints']):
                    if idx+1 < len(self.joints['spine_joints']):
                        cmds.parent(item, self.joints['spine_joints'][idx + 1])
                    else:
                        break
                # orient spine
                cmds.joint('root_bind', e=True, children=True, oj='xyz', secondaryAxisOrient='yup')
            except KeyError:
                pass

        # parent legs to root
        if cmds.objExists('root_bind'):
            if cmds.objExists('thigh_l_bind'):
                cmds.parent('thigh_l_bind', 'root_bind')

        else:
            pass

        if cmds.objExists('clavicle_l_bind'):
            if cmds.objExists('thumb_base_l_bind'):
                cmds.parent('thumb_base_l_bind', 'wrist_l_bind')
                cmds.parent('index_base_l_bind', 'wrist_l_bind')
                cmds.parent('middle_base_l_bind', 'wrist_l_bind')
                cmds.parent('ring_base_l_bind', 'wrist_l_bind')
                cmds.parent('pinky_base_l_bind', 'wrist_l_bind')
            else:
                pass
        else:
            pass

        if cmds.objExists('chest_bind'):
            cmds.parent('clavicle_l_bind', 'chest_bind')

        else:
            pass
        cmds.select(d=True)
        self.joints = {}

    def mirror_joints(self):
        #mirror joints
        if cmds.objExists('clavicle_l_bind'):
            cmds.mirrorJoint('clavicle_l_bind', mirrorBehavior=True, myz=True, searchReplace = ['_l_', '_r_'])
        elif cmds.objExists('thumb_base_l_bind'):
            cmds.mirrorJoint('thumb_base_l_bind', mirrorBehavior=True, myz=True, searchReplace=['_l_', '_r_'])
            cmds.mirrorJoint('index_base_l_bind', mirrorBehavior=True, myz=True, searchReplace=['_l_', '_r_'])
            cmds.mirrorJoint('middle_base_l_bind', mirrorBehavior=True, myz=True, searchReplace=['_l_', '_r_'])
            cmds.mirrorJoint('ring_base_l_bind', mirrorBehavior=True, myz=True, searchReplace=['_l_', '_r_'])
            cmds.mirrorJoint('pinky_base_l_bind', mirrorBehavior=True, myz=True, searchReplace=['_l_', '_r_'])
        else:
            pass
        pass

        if cmds.objExists('thigh_l_bind'):
            cmds.mirrorJoint('thigh_l_bind', mirrorBehavior=True, myz=True, searchReplace=['_l_', '_r_'])
        else:
            pass

    def orient_mid_joint(self, obj_start, obj_mid, obj_end):
            #make sure that the knee is oriented properly
            cmds.parent(obj_end, w = True)
            cmds.parent(obj_mid, w = True)
            locator = cmds.spaceLocator(n = 'orient')[0]
            first_obj = cmds.xform(obj_start, q=True, ws=True, t=True)
            second_obj = cmds.xform(obj_mid, q=True, ws=True, t=True)
            third_obj = cmds.xform(obj_end, q=True, ws=True, t=True)

            # make pole vector to be along direction of joints
            plane = cmds.polyPlane(sx=1, sy=1)
            cmds.delete(plane[0] + '.vtx[3]')

            cmds.xform(plane[0] + '.vtx[0]',ws = True, t = (first_obj[0], first_obj[1], first_obj[2]))
            cmds.xform(plane[0] + '.vtx[1]',ws = True, t = (second_obj[0], second_obj[1], second_obj[2]))
            cmds.xform(plane[0] + '.vtx[2]',ws = True, t = (third_obj[0], third_obj[1], third_obj[2]))
            cmds.moveVertexAlongDirection(plane[0] + '.vtx[1]', v = 10)

            vertex = cmds.xform(plane[0] + '.vtx[1]', q=True, ws=True, t=True)
            cmds.xform(locator, ws=True, t=(vertex[0], vertex[1], vertex[2]))

            cmds.setAttr(obj_mid + '.jointOrientX', 0)
            cmds.setAttr(obj_mid + '.jointOrientY', 0)
            cmds.setAttr(obj_mid + '.jointOrientZ', 0)

            aim = cmds.aimConstraint(obj_end, obj_mid, aim=[1.0, 0.0, 0.0], upVector=[0.0, 1.0, 0.0],
                                     wut='object', worldUpObject='orient')
            cmds.delete(aim)
            mid_joint_rotation = cmds.xform(obj_mid, ws = True, q = True, ro = True)

            cmds.setAttr(obj_mid + '.jointOrientX', mid_joint_rotation[0])
            cmds.setAttr(obj_mid + '.jointOrientY', mid_joint_rotation[1])
            cmds.setAttr(obj_mid + '.jointOrientZ', mid_joint_rotation[2])

            cmds.setAttr(obj_mid + '.rx', 0)
            cmds.setAttr(obj_mid + '.ry', 0)
            cmds.setAttr(obj_mid + '.rz', 0)

            #parent shin back
            cmds.parent(obj_mid, obj_start)
            cmds.parent(obj_end, obj_mid)

            #delete up object
            cmds.delete(locator)
            cmds.delete(plane)

    def make_finger_controls(self, base, mid, end, color):
        group = cmds.group(em=True, n='finger_controls')
        cmds.parent(group, 'controls')
        finger_ctl_base = cmds.circle(n = base + '_Ctl', r=1.5 ,nr = [1,0,0])[0]
        self.l.override_colors(finger_ctl_base, color)
        finger_ctl_base_Grp = cmds.group(finger_ctl_base)
        cmds.matchTransform(finger_ctl_base_Grp, base, pos=True, rot=True)
        cmds.parentConstraint(finger_ctl_base, base, mo=True)
        main_finger_ctl = cmds.circle(n = base + '_main_Ctl', r=1)
        main_finger_ctl_Grp = cmds.group(main_finger_ctl)
        cmds.matchTransform(main_finger_ctl_Grp, base, pos=True, rot=True)
        cmds.parentConstraint(main_finger_ctl, finger_ctl_base_Grp, mo=True)
        parent_obj = cmds.pickWalk(base, direction='up')
        if parent_obj[0] == base:
            pass
        else:
            cmds.parentConstraint(parent_obj, main_finger_ctl_Grp, mo=True)
        cmds.parent(finger_ctl_base_Grp, main_finger_ctl_Grp, 'finger_controls')

        finger_list = [mid, end]
        for obj in finger_list:
            finger_ctl = cmds.circle(n = obj + '_Ctl', r=1, nr = [1,0,0])
            self.l.override_colors(finger_ctl[0], color)
            finger_ctl_rotate = cmds.group(finger_ctl, n = str(finger_ctl) + '_Rotate')
            finger_ctl_Grp = cmds.group(finger_ctl_rotate)
            cmds.matchTransform(finger_ctl_Grp, obj, pos=True, rot=True)
            cmds.parentConstraint(finger_ctl, obj)

            parent_obj = cmds.pickWalk(obj, direction='up')
            cmds.parentConstraint(parent_obj, finger_ctl_Grp, mo=True)
            cmds.connectAttr(finger_ctl_base + '.rotate', finger_ctl_rotate + '.rotate')
            cmds.parent(finger_ctl_Grp, 'finger_controls')


    # build a rig
    def create_control_rig(self):
        if cmds.objExists('controls'):
            pass
        else:
            cmds.group(em=True, n='controls')
            cmds.group(em=True, n='IKs')
            cmds.group(em=True, n='extra')
            cmds.group(em=True, n='joints')

            main_control = cmds.circle(n = 'main_control', nr = [0,1,0], r = 20)[0]
            cmds.setAttr(main_control + '.lineWidth', 2)
            shape_main_control = cmds.listRelatives(main_control)[0]
            self.l.override_colors(shape_main_control, [1,0.7,0])
            cmds.parent('controls', 'IKs', 'joints',  main_control)
            cmds.group(em = True, n = 'RIG')
            cmds.parent(main_control, 'extra', 'RIG')

        self.reorient_joints()
        self.mirror_joints()

        # create leg rig
        if cmds.objExists('thigh_l_bind'):
            l = leg_rig.create_rig()
            l.create_leg_rig('l', 'root_bind', 'thigh_l_bind', 'shin_l_bind', 'ankle_l_bind', 'foot_l_driven', 'foot_l_end', 'heel_l_bind', [0.247,0,1])
            l.create_leg_rig('r', 'root_bind', 'thigh_r_bind', 'shin_r_bind', 'ankle_r_bind', 'foot_r_driven', 'foot_r_end', 'heel_r_bind', [1,0,0.034])
        else:
            pass

        # create arm rig
        if cmds.objExists('clavicle_l_bind'):
            a = arm_rig.create_arm_rig()
            a.make_arm_rig('l', 'clavicle_l_bind','shoulder_l_bind','elbow_l_bind', 'wrist_l_bind', [0.247,0,1])
            a.make_arm_rig('r', 'clavicle_r_bind','shoulder_r_bind','elbow_r_bind', 'wrist_r_bind', [1,0,0.034])
        else:
            pass

        if cmds.objExists('thumb_base_l_bind'):
            self.make_finger_controls('thumb_base_l_bind', 'thumb_mid_l_bind', 'thumb_end_l_bind', [0.7, 0,1])
            self.make_finger_controls('index_base_l_bind', 'index_mid_l_bind', 'index_end_l_bind',[0.7, 0,1])
            self.make_finger_controls('middle_base_l_bind', 'middle_mid_l_bind', 'middle_end_l_bind', [0.7, 0,1])
            self.make_finger_controls('ring_base_l_bind', 'ring_mid_l_bind', 'ring_end_l_bind', [0.7, 0,1])
            self.make_finger_controls('pinky_base_l_bind', 'pinky_mid_l_bind', 'pinky_end_l_bind', [0.7, 0,1])

            self.make_finger_controls('thumb_base_r_bind', 'thumb_mid_r_bind', 'thumb_end_r_bind', [1,0,0.33])
            self.make_finger_controls('index_base_r_bind', 'index_mid_r_bind', 'index_end_r_bind', [1,0,0.33])
            self.make_finger_controls('middle_base_r_bind', 'middle_mid_r_bind', 'middle_end_r_bind', [1,0,0.33])
            self.make_finger_controls('ring_base_r_bind', 'ring_mid_r_bind', 'ring_end_r_bind', [1,0,0.33])
            self.make_finger_controls('pinky_base_r_bind', 'pinky_mid_r_bind', 'pinky_end_r_bind', [1,0,0.33])
        else:
            pass

        # create spine rig
        if cmds.objExists('chest_bind'):
            s = spine_rig.create_spine_rig()
            s.make_spine_rig('root_bind', 'chest_bind', 'neck_bind', 'neck_02_bind', 'head_bind', [16, 0.57,0])
        else:
            pass
        cmds.select(d = True)

def main():
    auto_rig = auto_rig_ui()
    auto_rig.show()

main()




