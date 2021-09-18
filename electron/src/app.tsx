import { FormEvent, useState } from 'react';
import { render } from 'react-dom';
import { execFilePromise } from './preload';

declare global {
  interface Window {
    thoth: {
      runThoth: (path: string) => ReturnType<typeof execFilePromise>;
    };
  }
}

const App = (): JSX.Element => {
  const [fileName, setFileName] = useState('');
  const [output, setOutput] = useState('');

  const handleSubmit = (e: FormEvent): void => {
    e.preventDefault();
    window.thoth
      .runThoth(fileName)
      .then((result) => setOutput(result.stdout.toString()))
      .catch((reason) =>
        setOutput(`Command failed: ${JSON.stringify(reason)}`),
      );
  };

  return (
    <>
      <form onSubmit={handleSubmit}>
        <label>
          Enter file:{' '}
          <input
            type="text"
            value={fileName}
            onChange={(e) => setFileName(e.target.value)}
          />
        </label>
        <input type="submit" value="Submit" />
      </form>
      {output !== '' && <p>{output}</p>}
    </>
  );
};

render(<App />, document.getElementById('app'));
