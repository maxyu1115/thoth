import { FormEvent, useState } from 'react';
import { render } from 'react-dom';
import { getDirname, runThoth } from './preload';
import { CustomDropzone } from './components';

declare global {
  interface Window {
    thoth: {
      runThoth: typeof runThoth;
      getDirname: typeof getDirname;
    };
  }
}

const App = (): JSX.Element => {
  const [fileName, setFileName] = useState('');
  const [output, setOutput] = useState('');

  const handleSubmit = (e: FormEvent): void => {
    e.preventDefault();
    window.thoth
      .runThoth(window.thoth.getDirname(fileName))
      .then((result) => setOutput(result.stdout.toString()))
      .catch((reason) =>
        setOutput(`Command failed: ${JSON.stringify(reason)}`),
      );
  };

  return (
    <>
      <form onSubmit={handleSubmit}>
        <CustomDropzone setter={setFileName} />
        <input type="submit" value="Submit" />
      </form>
      {output !== '' && <p>{output}</p>}
    </>
  );
};

render(<App />, document.getElementById('app'));
