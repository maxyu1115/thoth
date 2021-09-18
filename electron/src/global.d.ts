import { getDirname, runThoth } from './preload';

declare global {
    interface Window {
      thoth: {
        runThoth: typeof runThoth;
        getDirname: typeof getDirname;
      };
    }
  }