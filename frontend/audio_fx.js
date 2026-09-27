/**
 * Indian Railways AI Prototype • Web Audio Synthesis & Cabin Chimes Module
 * Provides synthesized station chimes, signal alerts, and dispatch sounds
 * Author: SIH AI Prototype
 */

class RailAudioManager {
  constructor() {
    this.ctx = null;
    this.enabled = localStorage.getItem('rail_audio_enabled') !== 'false';
  }

  initContext() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) {
        this.ctx = new AudioCtx();
      }
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  toggleSound() {
    this.initContext();
    this.enabled = !this.enabled;
    localStorage.setItem('rail_audio_enabled', this.enabled ? 'true' : 'false');
    this.updateToggleButtons();
    if (this.enabled) {
      this.playChime();
    }
    return this.enabled;
  }

  updateToggleButtons() {
    document.querySelectorAll('.audio-toggle-btn').forEach(btn => {
      btn.innerHTML = this.enabled ? '<span>🔊</span><span>Audio ON</span>' : '<span>🔇</span><span>Muted</span>';
      btn.classList.toggle('audio-muted', !this.enabled);
    });
  }

  /**
   * Iconic Indian Railways Triple-Chime (Station Arrival / Departure)
   * Plays harmonic bell tones: 587Hz (D5) -> 880Hz (A5) -> 659Hz (E5)
   */
  playChime() {
    if (!this.enabled) return;
    this.initContext();
    if (!this.ctx) return;

    const notes = [
      { freq: 587.33, start: 0.0, dur: 0.45 }, // D5
      { freq: 880.00, start: 0.35, dur: 0.55 }, // A5
      { freq: 659.25, start: 0.75, dur: 0.85 }  // E5
    ];

    notes.forEach(note => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(note.freq, this.ctx.currentTime + note.start);

      // Bell envelope (quick attack, gradual resonant decay)
      const t = this.ctx.currentTime + note.start;
      gain.gain.setValueAtTime(0.001, t);
      gain.gain.exponentialRampToValueAtTime(0.22, t + 0.04);
      gain.gain.exponentialRampToValueAtTime(0.0001, t + note.dur);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(t);
      osc.stop(t + note.dur + 0.1);
    });
  }

  /**
   * High-Priority Red Signal Emergency Klaxon
   * Oscillating two-tone alert for signal drops and emergency braking
   */
  playRedSignalAlert() {
    if (!this.enabled) return;
    this.initContext();
    if (!this.ctx) return;

    const t = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();

    osc.type = 'sawtooth';
    // Rapid alternating siren between 750Hz and 480Hz
    osc.frequency.setValueAtTime(750, t);
    osc.frequency.setValueAtTime(480, t + 0.12);
    osc.frequency.setValueAtTime(750, t + 0.24);
    osc.frequency.setValueAtTime(480, t + 0.36);
    osc.frequency.setValueAtTime(750, t + 0.48);

    gain.gain.setValueAtTime(0.25, t);
    gain.gain.exponentialRampToValueAtTime(0.001, t + 0.65);

    osc.connect(gain);
    gain.connect(this.ctx.destination);

    osc.start(t);
    osc.stop(t + 0.7);
  }

  /**
   * Green Clear Track Whistle / Confirmation Chime
   */
  playClearSignalChime() {
    if (!this.enabled) return;
    this.initContext();
    if (!this.ctx) return;

    const t = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();

    osc.type = 'triangle';
    osc.frequency.setValueAtTime(523.25, t); // C5
    osc.frequency.exponentialRampToValueAtTime(1046.50, t + 0.25); // C6

    gain.gain.setValueAtTime(0.01, t);
    gain.gain.linearRampToValueAtTime(0.2, t + 0.05);
    gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.45);

    osc.connect(gain);
    gain.connect(this.ctx.destination);

    osc.start(t);
    osc.stop(t + 0.5);
  }

  /**
   * Subtle Futuristic Glass Tap for UI interaction
   */
  playTap() {
    if (!this.enabled) return;
    this.initContext();
    if (!this.ctx) return;

    const t = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(1200, t);
    gain.gain.setValueAtTime(0.08, t);
    gain.gain.exponentialRampToValueAtTime(0.001, t + 0.08);

    osc.connect(gain);
    gain.connect(this.ctx.destination);

    osc.start(t);
    osc.stop(t + 0.09);
  }
}

// Global Singleton Instance
window.railAudio = new RailAudioManager();

// Wire up any .audio-toggle-btn elements once DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.railAudio.updateToggleButtons();
  document.querySelectorAll('.audio-toggle-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      window.railAudio.toggleSound();
    });
  });

  // Enable audio context automatically on the user's first click anywhere on the page
  const unlockAudio = () => {
    window.railAudio.initContext();
    document.removeEventListener('click', unlockAudio);
    document.removeEventListener('keydown', unlockAudio);
  };
  document.addEventListener('click', unlockAudio, { once: true });
  document.addEventListener('keydown', unlockAudio, { once: true });
});
