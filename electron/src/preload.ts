import { contextBridge } from "electron";
import { execFile } from 'child_process';
import path from 'path';
import { promisify } from 'util';
 
const execFilePromise = promisify(execFile);

const runThoth = (filepath: string) => {
    const command = path.join(process.resourcesPath, "file");
    const args = ["-b", filepath];

    return execFilePromise(command, args);
}

contextBridge.exposeInMainWorld('thoth', {
    desktop: true,
    runThoth: runThoth,
})
