import { CustomWindow } from './custom-window';

declare let window: CustomWindow;

export interface InitializeSlidesOptions {
    readonly page: 'slides';
}

let currentSlide: number = 1;

function showSlide(slideNumber: number): void {
  // Hide all slides
  const slides: HTMLCollectionOf<Element> = document.getElementsByClassName('slide');
  for (let i = 0; i < slides.length; i++) {
    (slides[i] as HTMLElement).style.display = 'none';
  }
  // Show the selected slide
  (document.getElementById('slide' + slideNumber) as HTMLElement).style.display = 'block';
  currentSlide = slideNumber;
}

export function nextSlide(): void {
  if (currentSlide < totalSlides) {
    showSlide(currentSlide + 1);
  }
}

export function previousSlide(): void {
  if (currentSlide > 1) {
    showSlide(currentSlide - 1);
  }
}

export async function initializeSlides(_options: InitializeSlidesOptions) {
    document.addEventListener('keydown', function(event: KeyboardEvent): void {
        if (event.key === 'ArrowRight') {
          nextSlide();
        } else if (event.key === 'ArrowLeft') {
          previousSlide();
        }
      });

}
