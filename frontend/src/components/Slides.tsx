import React, { useState } from 'react';
import { Carousel } from 'react-responsive-carousel';
import 'react-responsive-carousel/lib/styles/carousel.min.css';

interface SlideInfo {
  order: number;
  path: string;
  text: string;
}

export const Slides = ({ slides }: { slides: SlideInfo[] }): JSX.Element => {
  const [value, setValue] = useState(0);

  const handleSlideChange = (index: number, item: React.ReactNode): void => {
    setValue(index);
  };

  return (
    <div>
      <Carousel showArrows={true} onChange={handleSlideChange}>
        {slides.map((info) => (
          <div key={info.order} className="each-slide">
            <img
              src={info.path}
              style={{ maxWidth: '20vw' }}
              alt="A portion of the slideshow"
            />
          </div>
        ))}
      </Carousel>
      <p>{slides[value].text}</p>
    </div>
  );
};
