import numpy as np
import wave, math
from collections import deque
import random
import argparse, pygame, os, sys
import matplotlib.pyplot as plt
import time

"""
Experiments from Python Playground:

1. Use the techniques you learned in this chapter to create a method that replicates the sound of two strings of different frequencies vibrating together. Remember, the Karplus-Strong algorithm produces sound amplitudes that can be added together (before scaling to 16-bit values for WAV file creation). Now add a time delay between the first and second string plucks.

2. Write a method to read music from a text file and generate musical notes. Then play the music using these notes. You can use a format where the note names are followed by integer rest time intervals, like this: C4 1 F4 2 G4 1 . . . .

3. Add a --piano command line option to the project. When the project is run with this option, the user should be able to press the A, S, D, F, and G keys on a keyboard to play the five musical notes. (Hint: use pygame.event.get and pygame.event.type.)

"""

# Notes used in Annihilation
pmNotes = {'E3':164, 'F3':174, 'G3':196, 'A3':220, 'B3':246, 'C4': 262, 'D4':293, 'Eb4': 311, 'F4': 349, 'G4':391, 'Bb4':466}

# G-major Scale
pmNotesG = {'G4':392, 'A4':440, 'B4':493, 'C5':523, 'D5':587, 'E5':659, 'F5#':739, 'G5':783}

# Minor Pentatonic Scale
peNotes = {'C4': 262, 'Eb': 311, 'F': 349, 'G':391, 'Bb':466}
gShowPlot = False

chords = {
    'G':['G4', 'B4', 'D5'],
    'A':['A4', 'C5', 'E5'],
    'C':['C5', 'E5', 'G5']
}

pygame.init()

def generate_note(freq):
    sRate = 44100
    nSamples = 44100
    N = int(sRate/freq)

    buf = deque([random.random() - 0.5 for i in range(N)])

    if gShowPlot:
        axline, = plt.plot(buf)

    samples = np.array([0]*nSamples, 'float32')
    for i in range(nSamples):
        samples[i] = buf[0]
        avg = 0.996 * 0.5 * (buf[0] + buf[1])
        buf.append(avg)
        buf.popleft()
        if gShowPlot:
            if i % 1000 == 0:
                axline.set_ydata(buf)
                plt.draw()

    samples = np.array(samples*32767, 'int16')
    return samples.tobytes()

def generate_double_note(freq1, freq2):
    sRate = 44100
    nSamples = 44100
    N1 = int(sRate/freq1)
    N2 = int(sRate/freq2)

    buf1 = deque([random.random() - 0.5 for i in range(N1)])
    buf2 = deque([random.random() - 0.5 for i in range(N2)])

    if gShowPlot:
            axline, = plt.plot(buf1)

    samples1 = np.array([0]*nSamples, 'float32')
    samples2 = np.array([0]*nSamples, 'float32')
    
    for i in range(nSamples):
        samples1[i] = buf1[0]
        buf1.append(0.996 * 0.5 * (buf1[0] + buf1[1]))
        buf1.popleft()

        if i > 10:

            samples2[i] = buf2[0]
            buf2.append(0.996 * 0.5 * (buf2[0] + buf2[1]))
            buf2.popleft()

        if gShowPlot:
            if i % 1000 == 0:
                axline.set_ydata(buf1)
                axline.set_ydata(buf2)
                plt.draw()

    netSamples = np.add(samples1, samples2)
    netSamples = np.array(netSamples*32767, 'int16')
    return netSamples

def writeWAVE(fname, data):
    f = wave.open(fname, 'wb')
    nChannels = 1
    sampleWidth = 2
    frameRate = 44100
    nFrames = 44100
    f.setparams((nChannels, sampleWidth, frameRate, nFrames, 'NONE', 'noncompressed'))
    f.writeframes(data)
    f.close()

class NotePlayer:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 2048)
        pygame.init()
        self.notes = {}

    def add(self, fname):
        self.notes[fname] = pygame.mixer.Sound(fname)

    def play(self, fname):
        try:
            self.notes[fname].play()
        except:
            print(fname + " not found!")

    def playRandom(self):
        index = random.randint(0, len(self.notes) - 1)
        note = list(self.notes.values())[index]
        note.play()

def get_notes(txtfile):
    with open(txtfile, 'r') as f:
        content = f.readline()

    notes = []

    for notenames in content.split():
        note = notenames[:notenames.index('-')]
        freq = pmNotes[note]
        interval = float(notenames[notenames.index('-')+1:])
        notes.append([note, freq, interval])

    return notes

def main():
    global gShowPlot
    parser = argparse.ArgumentParser(description="Generating notes...")
    
    parser.add_argument('--display', action='store_true', required=False)
    parser.add_argument('--play', action='store_true', required=False)
    parser.add_argument('--piano', action='store_true', required=False)
    parser.add_argument('--text-file', dest='txtfile', required=False)
    args = parser.parse_args()

    if args.display:
        gShowPlot = True
        plt.ion()

    nplayer = NotePlayer()

    if args.txtfile:
        print("Playing from %s" % (args.txtfile), "...")
        notes = get_notes(args.txtfile)
        for note in notes:
            filename = note[0] + '.wav'
            data = generate_note(note[1])

            if not os.path.exists(filename) or args.display:
                writeWAVE(filename, data)

            nplayer.add(filename)
            nplayer.play(filename)
            time.sleep(note[2])

    if args.piano:
        
        display = pygame.display.set_mode((300, 300))
        font = pygame.font.Font('freesansbold.ttf', 16)
        text = font.render('A: C4, S: Eb, D: F, F: G, G: Bb', True, (0, 0, 0), (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (150, 150)
        display.fill((255, 255, 255))
        display.blit(text, text_rect)

        pygame.display.update()
        notes = {pygame.K_a:'C4', pygame.K_s:'Eb', pygame.K_d:'F', pygame.K_f:'G', pygame.K_g:'Bb'}
        
        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key in notes:

                        freq = peNotes[notes[event.key]]
                        filename = notes[event.key] + '.wav'
                        if not os.path.exists(filename) or args.display:
                            writeWAVE(filename, generate_note(freq))
                        
                        nplayer.add(filename)
                        nplayer.play(filename)

    if args.display:

        print("Creating notes...")
        for name, freq in list(pmNotesG.items()):
            filename = name + ".wav"
            if not os.path.exists(filename) or args.display:
                data = generate_double_note(freq, freq)
                print('creating' + filename + ' ...')
                writeWAVE(filename, data)
            else:
                print('filename already created. skipping...')

            nplayer.add(name + '.wav')
            if args.display:
                nplayer.play(name + '.wav')
                time.sleep(0.5)

            if args.play:
                while True:
                    try:
                        nplayer.playRandom()
                        rest = np.random.choice([1, 2, 4, 8], 1, p=[0.15, 0.7, 0.1, 0.05])
                        time.sleep(0.25*rest[0])
                    except KeyboardInterrupt:
                        exit()

if __name__ == "__main__":
    main()
