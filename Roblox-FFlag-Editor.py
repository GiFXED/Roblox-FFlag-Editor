import os
import json
from PyQt5 import QtWidgets

class RobloxFFlagEditor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Roblox FFlag Editor - @GiFXED (Beta)")
        self.setFixedSize(400, 400)
        self.initUI()
        self.ensure_json_exists()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.tabs = QtWidgets.QTabWidget()
        self.basic_tab = QtWidgets.QWidget()
        self.advanced_tab = QtWidgets.QWidget()
        self.tabs.addTab(self.basic_tab, "Basic Controls")
        self.tabs.addTab(self.advanced_tab, "Advanced Controls")

        self.basic_layout = QtWidgets.QVBoxLayout(self.basic_tab)
        self.advanced_layout = QtWidgets.QVBoxLayout(self.advanced_tab)

        self.noclip_button = QtWidgets.QPushButton("Toggle Noclip")
        self.noclip_button.clicked.connect(lambda: self.toggle_fflag("Noclip", noclip_flags))
        self.basic_layout.addWidget(self.noclip_button)

        self.hip_height_label = QtWidgets.QLabel("Set Hip Height Value:")
        self.basic_layout.addWidget(self.hip_height_label)

        self.hip_height_input = QtWidgets.QSpinBox(self)
        self.hip_height_input.setRange(-500, 0)
        self.basic_layout.addWidget(self.hip_height_input)

        self.set_hip_height_button = QtWidgets.QPushButton("Set Hip Height")
        self.set_hip_height_button.clicked.connect(self.set_hip_height)
        self.basic_layout.addWidget(self.set_hip_height_button)

        self.network_ownership_button = QtWidgets.QPushButton("Set Network Ownership")
        self.network_ownership_button.clicked.connect(lambda: self.set_flags(network_ownership_flags))
        self.basic_layout.addWidget(self.network_ownership_button)

        self.gravity_button = QtWidgets.QPushButton("Set Low Gravity")
        self.gravity_button.clicked.connect(lambda: self.set_flags(low_gravity_flags))
        self.basic_layout.addWidget(self.gravity_button)

        self.log = QtWidgets.QTextEdit(self)
        self.log.setReadOnly(True)
        self.basic_layout.addWidget(self.log)

        self.custom_fflag_input = QtWidgets.QLineEdit(self)
        self.custom_fflag_input.setPlaceholderText("Enter Custom FFlag")
        self.advanced_layout.addWidget(self.custom_fflag_input)

        self.custom_value_input = QtWidgets.QLineEdit(self)
        self.custom_value_input.setPlaceholderText("Enter Custom Value")
        self.advanced_layout.addWidget(self.custom_value_input)

        self.add_custom_fflag_button = QtWidgets.QPushButton("Add Custom FFlag")
        self.add_custom_fflag_button.clicked.connect(self.add_custom_fflag)
        self.advanced_layout.addWidget(self.add_custom_fflag_button)

        self.log_advanced = QtWidgets.QTextEdit(self)
        self.log_advanced.setReadOnly(True)
        self.advanced_layout.addWidget(self.log_advanced)

        self.beta_warning = QtWidgets.QLabel("This is a beta version. Report bugs on the GitHub repo.")
        self.basic_layout.addWidget(self.beta_warning)

        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.log.append("FFlag Editor initialized. Make changes and restart Roblox to see the effects.")

    def get_roblox_folder(self):
        for root, dirs, files in os.walk(os.path.join(os.getenv("LOCALAPPDATA"), "Roblox", "Versions")):
            if "RobloxPlayerBeta.exe" in files:
                return root
        return None

    def create_client_settings(self):
        folder = self.get_roblox_folder()
        if folder is None:
            self.log.append("Roblox installation not found.")
            return None
        
        settings_folder = os.path.join(folder, "ClientSettings")
        if not os.path.exists(settings_folder):
            os.makedirs(settings_folder)
            self.log.append(f"Created ClientSettings folder at: {settings_folder}")
        
        return settings_folder

    def ensure_json_exists(self):
        settings_folder = self.create_client_settings()
        if settings_folder:
            json_path = os.path.join(settings_folder, "ClientAppSettings.json")
            if not os.path.exists(json_path):
                with open(json_path, 'w') as f:
                    json.dump({}, f)
                    self.log.append(f"Initialized JSON at {json_path}. Restart Roblox to see changes.")

    def save_json(self, data):
        settings_folder = self.create_client_settings()
        if settings_folder:
            json_path = os.path.join(settings_folder, "ClientAppSettings.json")
            with open(json_path, 'w') as f:
                json.dump(data, f, indent=4)
                self.log.append(f"Saved JSON to {json_path}. Restart Roblox to see changes.")

    def load_json(self):
        settings_folder = self.create_client_settings()
        json_path = os.path.join(settings_folder, "ClientAppSettings.json")
        try:
            with open(json_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.log.append(f"Error loading JSON: {e}")
            self.ensure_json_exists()
            return {}

    def toggle_fflag(self, flag_name, flag_data):
        data = self.load_json()

        if flag_name == "Noclip":
            if "FFlagDebugSimDefaultPrimalSolver" in data:
                self.log.append("Disabling Noclip...")
                data.pop("FFlagDebugSimDefaultPrimalSolver", None)
                data.pop("DFIntMaximumFreefallMoveTimeInTenths", None)
                data.pop("DFIntDebugSimPrimalStiffness", None)
            else:
                self.log.append("Enabling Noclip...")
                data.update(flag_data[0])

        self.save_json(data)

    def set_hip_height(self):
        hip_height_value = self.hip_height_input.value()
        data = self.load_json()
        data["DFIntMaxAltitudePDStickHipHeightPercent"] = str(hip_height_value)
        self.save_json(data)
        self.log.append(f"Set Hip Height to {hip_height_value}.")

    def set_flags(self, flag_data):
        data = self.load_json()
        data.update(flag_data)
        self.save_json(data)

    def add_custom_fflag(self):
        custom_fflag = self.custom_fflag_input.text()
        custom_value = self.custom_value_input.text()

        if custom_fflag and custom_value:
            data = self.load_json()
            data[custom_fflag] = custom_value
            self.save_json(data)
            self.log_advanced.append(f"Added custom FFlag: {custom_fflag} = {custom_value}")
        else:
            self.log_advanced.append("Please enter both FFlag and value.")

noclip_flags = [{
    "FFlagDebugSimDefaultPrimalSolver": "True",
    "DFIntMaximumFreefallMoveTimeInTenths": "1000",
    "DFIntDebugSimPrimalStiffness": "0"
}]

network_ownership_flags = {
    "DFIntMinClientSimulationRadius": "2147000000",
    "DFIntMinimalSimRadiusBuffer": "2147000000",
    "DFIntMaxClientSimulationRadius": "2147000000"
}

low_gravity_flags = {
    "FFlagDebugSimDefaultPrimalSolver": "True",
    "DFIntDebugSimPrimalLineSearch": "3"
}

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = RobloxFFlagEditor()
    window.show()
    app.exec_()
