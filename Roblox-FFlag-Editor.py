import os
import json
from PyQt5 import QtWidgets
from PyQt5 import QtCore

class RobloxFFlagEditor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Roblox FFlag Editor - @GiFXED (Beta 3.5)")
        self.setFixedSize(400, 600)
        self.initUI()
        self.ensure_json_exists()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.tabs = QtWidgets.QTabWidget()
        self.basic_tab = QtWidgets.QWidget()
        self.advanced_tab = QtWidgets.QWidget()
        self.info_tab = QtWidgets.QWidget()
        self.tabs.addTab(self.basic_tab, "Basic Controls")
        self.tabs.addTab(self.advanced_tab, "Advanced Controls")
        self.tabs.addTab(self.info_tab, "info")

        self.basic_layout = QtWidgets.QVBoxLayout(self.basic_tab)
        self.advanced_layout = QtWidgets.QVBoxLayout(self.advanced_tab)
        self.info_layout = QtWidgets.QVBoxLayout(self.info_tab)
        
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

        self.no_animations_button = QtWidgets.QPushButton("No Animations")
        self.no_animations_button.clicked.connect(lambda: self.set_flags(no_animations_flags))
        self.basic_layout.addWidget(self.no_animations_button)

        self.xray_button = QtWidgets.QPushButton("Xray")
        self.xray_button.clicked.connect(lambda: self.set_flags(xray_flags))
        self.basic_layout.addWidget(self.xray_button)

        self.disable_telemetry_button = QtWidgets.QPushButton("Disable Telemetry")
        self.disable_telemetry_button.clicked.connect(lambda: self.set_flags(disable_telemetry_flags))
        self.basic_layout.addWidget(self.disable_telemetry_button)

        self.disable_touch_events_button = QtWidgets.QPushButton("Disable touch events")
        self.disable_telemetry_button.clicked.connect(lambda: self.set_flags(disable_touch_events_flags))
        self.basic_layout.addWidget(self.disable_touch_events_button)

        self.disable_ads_button = QtWidgets.QPushButton("Disable In-game Ads")
        self.disable_ads_button.clicked.connect(lambda: self.toggle_fflag("Disable In-game Ads", disable_ads_flags))
        self.basic_layout.addWidget(self.disable_ads_button)

        self.disable_remote_events_button = QtWidgets.QPushButton("Disable Remote Events")
        self.disable_remote_events_button.clicked.connect(lambda: self.toggle_fflag("Disable Remote Events", disable_remote_events_flags))
        self.basic_layout.addWidget(self.disable_remote_events_button)

        self.max_zoom_label = QtWidgets.QLabel("Set Max Zoom Distance:")
        self.basic_layout.addWidget(self.max_zoom_label)

        self.max_zoom_input = QtWidgets.QSpinBox(self)
        self.max_zoom_input.setRange(10, 69420)
        self.basic_layout.addWidget(self.max_zoom_input)

        self.set_zoom_button = QtWidgets.QPushButton("Set Max Zoom Distance")
        self.set_zoom_button.clicked.connect(self.set_zoom_distance)
        self.basic_layout.addWidget(self.set_zoom_button)

        self.clear_file_button = QtWidgets.QPushButton("Clear fflag File")
        self.clear_file_button.clicked.connect(self.clear_json)
        self.basic_layout.addWidget(self.clear_file_button)

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

        self.modify_custom_fflag_button = QtWidgets.QPushButton("Modify Custom FFlag")
        self.modify_custom_fflag_button.clicked.connect(self.modify_custom_fflag)
        self.advanced_layout.addWidget(self.modify_custom_fflag_button)

        self.delete_custom_fflag_button = QtWidgets.QPushButton("Delete Custom FFlag")
        self.delete_custom_fflag_button.clicked.connect(self.delete_custom_fflag)
        self.advanced_layout.addWidget(self.delete_custom_fflag_button)

        self.log_advanced = QtWidgets.QTextEdit(self)
        self.log_advanced.setReadOnly(True)
        self.advanced_layout.addWidget(self.log_advanced)

        self.info_label = QtWidgets.QLabel(
        "Roblox FFlag Editor\n"
        "Developer: @Teemsploit\n"
        "If you find this repository useful, don't forget to star!\n"
        "Report any bugs on GitHub."
        "\n\n\n Contact:\nEmail: gifxed@proton.me\nDiscord: teemsploit\nYoutube: Teemsploit"
    )
        self.info_label.setAlignment(QtCore.Qt.AlignCenter)
        self.info_layout.addWidget(self.info_label)

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

    def set_zoom_distance(self):
        zoom_distance = self.max_zoom_input.value()
        data = self.load_json()
        data["FIntCameraMaxZoomDistance"] = str(zoom_distance)
        self.save_json(data)
        self.log.append(f"Set Max Zoom Distance to {zoom_distance}.")

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

    def modify_custom_fflag(self):
        custom_fflag = self.custom_fflag_input.text()
        custom_value = self.custom_value_input.text()

        if custom_fflag and custom_value:
            data = self.load_json()
            if custom_fflag in data:
                data[custom_fflag] = custom_value
                self.save_json(data)
                self.log_advanced.append(f"Modified custom FFlag: {custom_fflag} = {custom_value}")
            else:
                self.log_advanced.append(f"FFlag {custom_fflag} does not exist.")
        else:
            self.log_advanced.append("Please enter both FFlag and value.")

    def delete_custom_fflag(self):
        custom_fflag = self.custom_fflag_input.text()

        if custom_fflag:
            data = self.load_json()
            if custom_fflag in data:
                data.pop(custom_fflag)
                self.save_json(data)
                self.log_advanced.append(f"Deleted custom FFlag: {custom_fflag}")
            else:
                self.log_advanced.append(f"FFlag {custom_fflag} does not exist.")
        else:
            self.log_advanced.append("Please enter the FFlag to delete.")

    def clear_json(self):
        data = {}
        self.save_json(data)
        self.log.append("Cleared entire ClientAppSettings.json file.")

noclip_flags = {
    "FFlagDebugSimDefaultPrimalSolver": "True",
    "DFIntMaximumFreefallMoveTimeInTenths": "99999",
    "DFIntDebugSimPrimalStiffness": "0"
}

network_ownership_flags = {
    "DFIntMinClientSimulationRadius": "2147000000",
    "DFIntMinimalSimRadiusBuffer": "2147000000",
    "DFIntMaxClientSimulationRadius": "2147000000"
}

low_gravity_flags = {
    "FFlagDebugSimDefaultPrimalSolver": "True",
    "DFIntDebugSimPrimalLineSearch": "3"
}

no_animations_flags = {
    "DFIntReplicatorAnimationTrackLimitPerAnimator": "-1"
}

xray_flags = {
    "DFIntCullFactorPixelThresholdMainViewHighQuality": "10000",
    "DFIntCullFactorPixelThresholdMainViewLowQuality": "10000",
    "DFIntCullFactorPixelThresholdShadowMapHighQuality": "10000",
    "DFIntCullFactorPixelThresholdShadowMapLowQuality": "10000"
}

disable_telemetry_flags = {
    "FFlagDebugDisableTelemetryEphemeralCounter": "True",
    "FFlagDebugDisableTelemetryEphemeralStat": "True",
    "FFlagDebugDisableTelemetryEventIngest": "True",
    "FFlagDebugDisableTelemetryPoint": "True",
    "FFlagDebugDisableTelemetryV2Counter": "True",
    "FFlagDebugDisableTelemetryV2Event": "True",
    "FFlagDebugDisableTelemetryV2Stat": "True"
}

disable_touch_events_flags = {
    "DFIntTouchSenderMaxBandwidthBps": "-1"
}

disable_ads_flags = {
    "FFlagAdServiceEnabled": "False"
}

disable_remote_events_flags = {
    "DFIntRemoteEventSingleInvocationSizeLimit": "1"
}

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = RobloxFFlagEditor()
    window.show()
    app.exec_()
