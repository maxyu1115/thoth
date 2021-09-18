import { FormEvent, useState } from 'react';
import {render} from 'react-dom';

declare global {
    interface Window { thoth: { runThoth: (path: string) => Promise<{
        stdout: string;
        stderr: string;
    }> } }
}

const App = () => {
    const [fileName, setFileName] = useState("");
    const [output, setOutput] = useState("");

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        window.thoth.runThoth(fileName).then(result => setOutput(result.stdout));
    };

    return (
        <>
        <form onSubmit={handleSubmit}>
            <label>Enter file: <input type="text" value={fileName} onChange={e => setFileName(e.target.value)} /></label>
            <input type="submit" value="Submit" />
        </form>
        {output != "" && <p>{output}</p>}
        </>
    );
}

render(<App />, document.getElementById("app"));