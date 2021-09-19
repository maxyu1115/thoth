export const getSpeechJsonPath = (videoFileName: string): string =>
  `json/${videoFileName.replaceAll('.', '_')}_speech.json`;

export const getOcrJsonPath = (videoFileName: string): string =>
  `json/${videoFileName.replaceAll('.', '_')}_ocr.json`;
