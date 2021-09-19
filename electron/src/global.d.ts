import path from 'path';
import { runThoth } from './preload';

declare global {
  interface Window {
    thoth: {
      runThoth: typeof runThoth;
      getDirname: typeof path.dirname;
      tempPath: string;
      joinPaths: typeof path.join;
      getBasename: typeof path.basename;
    };
  }
}
