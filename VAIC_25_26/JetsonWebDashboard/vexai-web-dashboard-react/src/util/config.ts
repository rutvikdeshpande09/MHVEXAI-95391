import { Element } from "../lib/types";
import { images } from "./images";

/**
 * General configuration for the application
 */
export const config = {
  socketIP: "10.42.0.1",
  socketPort: "3030",

  /**
   * Default image width captured by the camera on the robot
   */
  SCALE_X: 640,

  /**
   * Default image height captured by the camera on the robot
   */
  SCALE_Y: 480,

  /**
   * Rate at which the data services polls for data (ms)
   */
  pollingInterval: 60,
  logDataResponse: false,
  detectOutOfBoundsElements: true,
  colors: {
    red: "#D22630",
    darkRed: "#971c22",
    gray: "#939597",
    darkGray: "#58585B",
    darkerGray: "#111111",
    blue: "#0077C8",
    darkBlue: "#004d80",
    black: "#000000",
    white: "#F4F2FF",
    orange: "#fca503",
    darkOrange: "#bf7e04",
    purple: "#7466F1",
    darkPurple: "#433b87",
    grayPurple: "#293045",
  },
  field: {
    dimension: 3.6576, // meters
    oov: 0.1,
    texture: images.field,
    scale: 1.5,
    compass: {
      texture: images.map.compass,
      scale: 0.23,
      ringPositionCorrectionX: 0.1,
      lineScale: 0.03,
      numberOffset: 0.045,
      numberScale: 0.017,
    },
    fog: {
      opacity: 0.75,
    },
    ruler: {
      texture: images.map.ruler,
      xySidebarOffset: 0.26,
      xySidebarMarkersOffset: 0.22,
      xySidebarArrowOffset: 0.22,
      xySidebarSizeMultiplier: 0.025,
      arrowScale: 0.1,
    },
    robot: {
      length: 0.4191, // meters
      width: 0.3175, // meters
      scale: 1.5,
      texture: images.robot,
      textureWidth: 1024, // pixels
      textureHeight: 1024, // pixels
      fov: 50,
    },
  },
  elements: {
    textures: {
      [Element.RedYellowPin]: images.elements.pin,
      [Element.Cup]: images.elements.cups,
      [Element.BlueYellowPin]: images.elements.pin,
      [Element.YellowPin]: images.elements.pin,
      [Element.RedBluePin]: images.elements.pin,
    },
    size: {
      [Element.RedYellowPin]: {
        height: 0.08255,
        width: 0.08255,
        scale: 2.0,
      },
      [Element.Cup]: {
        height: 0.08255,
        width: 0.08255,
        scale: 2.0,
      },
      [Element.BlueYellowPin]: {
        height: 0.08255,
        width: 0.08255,
        scale: 2.0
      },
      [Element.YellowPin]: {
        height: 0.08255,
        width: 0.08255,
        scale: 2.0
      },
      [Element.RedBluePin]: {
        height: 0.08255,
        width: 0.08255,
        scale: 2.0
      },
    },
    borderColors: {
      [Element.RedYellowPin]: "rgba(255, 165, 0, .8)",
      [Element.Cup]: "rgba(0, 200, 0, .8)",
      [Element.BlueYellowPin]: "rgba(0, 119, 200, .8)",
      [Element.YellowPin]: "rgba(255, 220, 0, .8)",
      [Element.RedBluePin]: "rgba(162, 107, 255, .8)",
    },
    backgroundColors: {
      [Element.RedYellowPin]: "rgba(255, 165, 0, .3)",
      [Element.Cup]: "rgba(0, 200, 0, .3)",
      [Element.BlueYellowPin]: "rgba(0, 119, 200, .3)",
      [Element.YellowPin]: "rgba(255, 220, 0, .3)",
      [Element.RedBluePin]: "rgba(162, 107, 255, .3)",
    },
    label: {
      textColors: {
        white: "rgba(255, 255, 255, 1)",
        black: "rgba(0, 0, 0, 1)",
      },
      text: {
        [Element.RedYellowPin]: "RedYellowPin",
        [Element.Cup]: "Cup",
        [Element.BlueYellowPin]: "BlueYellowPin",
        [Element.YellowPin]: "YellowPin",
        [Element.RedBluePin]: "RedBluePin",
      },
    },
  },
};
