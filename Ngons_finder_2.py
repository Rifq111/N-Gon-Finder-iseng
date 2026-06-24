import maya.cmds as cmds
import maya.OpenMayaUI as omui

from PySide6 import QtWidgets
from shiboken6 import wrapInstance


# =========================
# MAYA MAIN WINDOW
# =========================

def get_maya_main_window():
    ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QtWidgets.QWidget)


# =========================
# CORE N-GON FUNCTION
# =========================

def find_ngons(select_faces=True):
    cmds.select(clear=True)

    meshes = cmds.ls(type="mesh", long=True)
    ngon_faces = []
    mesh_report = {}

    for mesh in meshes:
        transform = cmds.listRelatives(mesh, parent=True, fullPath=True)[0]
        face_count = cmds.polyEvaluate(mesh, face=True)

        for i in range(face_count):
            face = f"{transform}.f[{i}]"
            edges = cmds.polyListComponentConversion(face, toEdge=True)
            edges = cmds.filterExpand(edges, sm=32)

            if edges and len(edges) > 4:
                ngon_faces.append(face)
                mesh_report.setdefault(transform, 0)
                mesh_report[transform] += 1

    if select_faces and ngon_faces:
        cmds.select(ngon_faces)

    return ngon_faces, mesh_report

    





# =========================
# UI
# =========================

class IsengNgonFinder(QtWidgets.QDialog):

    def __init__(self, parent=get_maya_main_window()):
        super().__init__(parent)
        self.setWindowTitle("-Iseng- N-Gon Finder V1")
        self.setFixedSize(380, 300)
        self.build_ui()


    def build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.lbl_select_info = QtWidgets.QLabel("V1")
        layout.addWidget(self.lbl_select_info)

        self.chk_select = QtWidgets.QCheckBox("Select N-gon faces")
        self.chk_select.setChecked(True)
        layout.addWidget(self.chk_select)

        # >>> TEKS DI BAWAH CHECKBOX <<<
        self.lbl_select_info = QtWidgets.QLabel(
            "Turn on the X-ray view first to make it easier."
        )
        self.lbl_select_info.setWordWrap(True)
        self.lbl_select_info.setStyleSheet("color: #01ffff; font-size: 11px;")
        layout.addWidget(self.lbl_select_info)
        # >>> END <<<


        self.btn_scan = QtWidgets.QPushButton("SCAN SCENE")
        self.btn_scan.setFixedHeight(40)
        self.btn_scan.clicked.connect(self.run_scan)
        layout.addWidget(self.btn_scan)

        layout.addSpacing(10)

        self.output = QtWidgets.QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)


    def run_scan(self):
        self.output.clear()

        faces, report = find_ngons(self.chk_select.isChecked())

        if not faces:
            self.output.setText("✔ No N-gons found\nScene is clean 👍")
            return

        result = []
        result.append(f"⚠ N-gons found: {len(faces)}\n")

        for mesh, count in report.items():
            result.append(f"{mesh} : {count} N-gons")

        self.output.setText("\n".join(result))



# =========================
# ENTRY POINT
# =========================

def run():
    global td_ngon_ui
    try:
        td_ngon_ui.close()
        td_ngon_ui.deleteLater()
    except:
        pass

    td_ngon_ui = TDNgonFinder()
    td_ngon_ui.show()
