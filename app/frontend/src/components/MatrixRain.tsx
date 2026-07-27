import { useEffect, useRef } from 'react';

const katakana =
  'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン';

export function MatrixRain() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReduced) return;

    let animId: number;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const cvs: HTMLCanvasElement = canvas;
    const context: CanvasRenderingContext2D = ctx;

    let columns: number[] = [];
    let dropY: number[] = [];
    let frameCount = 0;

    function resize() {
      cvs.width = window.innerWidth;
      cvs.height = window.innerHeight;
      columns = [];
      dropY = [];
      const colCount = Math.floor(cvs.width / 20);
      for (let i = 0; i < colCount; i++) {
        columns[i] = 1;
        dropY[i] = Math.floor(Math.random() * cvs.height);
      }
    }

    resize();
    window.addEventListener('resize', resize);

    function draw() {
      frameCount++;
      if (frameCount % 3 !== 0) {
        animId = requestAnimationFrame(draw);
        return;
      }

      context.fillStyle = 'rgba(10, 10, 15, 0.05)';
      context.fillRect(0, 0, cvs.width, cvs.height);

      context.font = '16px monospace';

      for (let i = 0; i < columns.length; i++) {
        const char = katakana[Math.floor(Math.random() * katakana.length)];
        const x = i * 20;
        const y = dropY[i] * 20;

        context.fillStyle = `rgba(0, 255, 65, ${0.3 + Math.random() * 0.5})`;
        context.fillText(char, x, y);

        if (y > cvs.height && Math.random() > 0.975) {
          dropY[i] = 0;
        }
        dropY[i]++;
      }

      animId = requestAnimationFrame(draw);
    }

    draw();

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener('resize', resize);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: 'fixed',
        inset: 0,
        zIndex: 0,
        pointerEvents: 'none',
        opacity: 0.4,
      }}
    />
  );
}
