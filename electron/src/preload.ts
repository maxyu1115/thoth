import { contextBridge } from "electron";
import { execFile } from 'child_process';
import path from 'path';
import { promisify } from 'util';
 
const execFilePromise = promisify(execFile);

const runThoth = (filepath: string) => {
    const command = path.join(process.resourcesPath, "thoth_engine");
    const args = ["--target", filepath];

    return execFilePromise(command, args);
}

contextBridge.exposeInMainWorld('thoth', {
    desktop: true,
    runThoth: runThoth,
})
