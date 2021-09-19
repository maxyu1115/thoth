import { Slide } from 'react-slideshow-image';

interface SlideInfo {
  order: number;
  path: string;
}

export const Slides = ({ slides }: { slides: SlideInfo[] }): JSX.Element => {
  return (
    <div>
      <Slide easing="ease">
        {slides.map((info) => (
          <div key={info.order} className="each-slide">
            <img src={info.path} alt="A portion of the slideshow" />
          </div>
        ))}
      </Slide>
    </div>
  );
};
