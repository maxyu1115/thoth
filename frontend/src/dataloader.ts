const BASE_URL = 'http://10.119.176.254:8000/';

export const search = async (
  phrase: string,
): Promise<any | { errorReason: string }> => {
  const request = new Request(
    new URL(`/search?phrase=${phrase}`, BASE_URL).href,
  );
  const options = {
    method: 'GET',
  };
  return await fetch(request, options)
    .then(async (res) => await res.json())
    .catch((error) => ({
      errorReason: JSON.stringify(error),
    }));
};

export const getFileByPath = async (
  path: string,
): Promise<Blob | { errorReason: string }> => {
  const request = new Request(new URL(`/storage/${path}`, BASE_URL).href);
  const options = {
    method: 'GET',
  };
  return await fetch(request, options)
    .then(async (res) => await res.blob())
    .catch((error) => ({
      errorReason: JSON.stringify(error),
    }));
};

export const uploadVideo = async (
  file: File,
  isAnimated: boolean,
): Promise<any | { errorReason: string }> => {
  console.log(file);
  const data = new FormData();
  const vidTypeParam = `vid-type=${
    isAnimated ? 'animated_slides' : 'unanimated_slides'
  }`;
  const request = new Request(
    new URL(`/upload_video?${vidTypeParam}`, BASE_URL).href,
  );
  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'multipart/form',
      Connection: 'keep-alive',
    },
  };

  data.append('file', file);

  return await fetch(request, {
    ...options,
    body: data,
  })
    .then(async (res) => await res.json())
    .then(async (res) => console.log(res))
    .catch((error) => {
      console.error(error);

      return { errorReason: JSON.stringify(error) };
    });
};

export const getDirData = async (
  path: string,
): Promise<any | { errorReason: string }> => {
  const request = new Request(
    new URL(`/directory-data/${path}`, BASE_URL).href,
  );
  const options = {
    method: 'GET',
  };

  return await fetch(request, options)
    .then(async (res) => await res.json())
    .catch((error) => ({
      errorReason: JSON.stringify(error),
    }));
};

export const getStatus = async (path: string): Promise<any> => {
  const request = new Request(new URL(`/status/${path}`, BASE_URL).href);
  const options = {
    method: 'GET',
  };

  return await fetch(request, options)
    .then(async (res) => await res.json())
    .catch((error) => ({
      errorReason: JSON.stringify(error),
    }));
};
