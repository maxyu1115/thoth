import React, { useMemo } from 'react';
import { DropEvent, useDropzone } from 'react-dropzone';

const baseStyle = {
  flex: 1,
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  padding: '20px',
  borderWidth: 2,
  borderRadius: 2,
  borderColor: '#eeeeee',
  borderStyle: 'dashed',
  backgroundColor: '#fafafa',
  color: '#bdbdbd',
  outline: 'none',
  transition: 'border .24s ease-in-out',
  width: '75%',
  height: '65%',
};

const activeStyle = {
  borderColor: '#2196f3',
};

const acceptStyle = {
  borderColor: '#00e676',
};

const rejectStyle = {
  borderColor: '#ff1744',
};

export const CustomDropzone = ({
  onDropAccepted,
}: {
  onDropAccepted?: <T extends File>(files: T[], event: DropEvent) => void;
}): JSX.Element => {
  const {
    getRootProps,
    getInputProps,
    isDragActive,
    isDragAccept,
    isDragReject,
  } = useDropzone({
    accept: ['video/*'],
    maxFiles: 1,
    onDropAccepted: onDropAccepted,
  });

  const style = useMemo(
    () => ({
      ...baseStyle,
      ...(isDragActive ? activeStyle : {}),
      ...(isDragAccept ? acceptStyle : {}),
      ...(isDragReject ? rejectStyle : {}),
    }),
    [isDragActive, isDragReject, isDragAccept],
  );

  return (
    <section style={{ width: '100%', height: '100%' }}>
      <div style={style as React.CSSProperties} {...getRootProps()}>
        <input {...getInputProps()} />
        <p>Drag your video here, or click to select a file</p>
      </div>
    </section>
  );
};
