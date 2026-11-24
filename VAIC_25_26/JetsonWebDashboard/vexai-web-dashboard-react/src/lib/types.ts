export enum Element {
  RedYellowPin = 0,
  Cup = 1,
  BlueYellowPin = 2,
  YellowPin = 3,
  RedBluePin = 4,
}

export enum Direction {
  X = 0,
  Y = 1,
}

export interface Theme {
  id: string;
  componentBackground: string;
  font: string;
  control: string;
  controlHover: string;
}
