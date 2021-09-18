import { FormEvent, useState } from 'react';
import { render } from 'react-dom';
import { getDirname, runThoth } from './preload';
import Dropzone from 'react-dropzone';

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
        <label htmlFor="drop">Upload file here:</label>
        <Dropzone
          onDrop={(acceptedFiles) => setFileName(acceptedFiles[0]?.path ?? '')}
        >
          {({ getRootProps, getInputProps }) => (
            <section>
              <div
                style={{
                  width: '800px',
                  height: '600px',
                  borderStyle: 'dotted',
                  textAlign: 'center',
                }}
                {...getRootProps()}
              >
                <input id="drop" {...getInputProps()} />
                <p>
                  Drag &lsquo;n&rsquo; drop some files here, or click to select
                  files
                </p>
              </div>
            </section>
          )}
        </Dropzone>
        <input type="submit" value="Submit" />
      </form>
      {output !== '' && <p>{output}</p>}
    </>
  );
};

render(<App />, document.getElementById('app'));
