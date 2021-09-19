import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { uploadVideo } from '../dataloader';

export function MyDropzone(): JSX.Element {
  const onDrop = useCallback((acceptedFiles) => {
    uploadVideo(acceptedFiles[0], true)
      .then((res) => console.log(res))
      .catch((err) => console.error(err));
  }, []);
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <div {...getRootProps()}>
      <input {...getInputProps()} />
      {isDragActive ? (
        <p>Drop the files here ...</p>
      ) : (
        <p>Drag 'n' drop some files here, or click to select files</p>
      )}
    </div>
  );
}
