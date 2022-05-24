import { CapacitorConfig } from "@capacitor/cli";

const config: CapacitorConfig = {
  appId: "de.danielgrams.cityservice",
  appName: "CityService",
  webDir: "../project/static/frontend",
  bundledWebRuntime: false,
  backgroundColor: "#009688",
  ios: {
    contentInset: "always",
  },
  server: {
    cleartext: true,
  },
  plugins: {
    PushNotifications: {
      presentationOptions: ["badge", "sound", "alert"],
    },
  },
};

export default config;
