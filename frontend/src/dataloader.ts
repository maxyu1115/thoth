import axios from 'axios';

const BASE_URL = 'http://10.119.176.254:8000';

export const search = async (
  phrase: string,
): Promise<any | { errorReason: string }> => {
  return await axios
    .get(`${BASE_URL}/search?phrase=${phrase}`)
    .then((response) => {
      console.log(response);

      return response;
    })
    .catch((reason) => {
      console.log(reason);

      return {
        errorReason: reason,
      };
    });
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
  const data = new FormData();
  const vidType = isAnimated ? 'animated_slides' : 'unanimated_slides';

  data.append('file', file);

  return await axios
    .post(`${BASE_URL}/upload-video?vid-type=${vidType}`, data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    .then((response) => {
      console.log(response);

      return response;
    })
    .catch((reason) => {
      console.log(reason);

      return {
        errorReason: reason,
      };
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
