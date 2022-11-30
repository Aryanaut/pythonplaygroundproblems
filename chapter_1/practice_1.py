import plistlib
import numpy as np
import matplotlib.pyplot as plt
import argparse as arg

def find_duplicates(file):
    with open(file, 'rb') as f:
            plist = plistlib.load(f)

    tracks = plist['Tracks']

    tracknames = {}
    for trackID, track in tracks.items():
        try:
            name = track['Name']
            time = track['Total Time']
            if name in tracknames:
                if time//1000 == tracknames[name][0]//1000:
                    count = tracknames[name][1]
                    tracknames[name] = (time, count+1)
            else:
                tracknames[name] = (time, 1)
        except KeyboardInterrupt:
            print("Exiting...")
            break

def extract_dup(tracknames):
    dups = []
    for keys, values in tracknames.items():
        if values[1] > 1:
            dups.append((values[1], keys))

        if len(dups) > 0:
            print("Found %d duplicates. Track names saved to d.txt"%len(dups))

        else:
            print("No duplicates.")

        with open("d.txt", 'w') as f:
            for val in dups:
                f.write("[%d] %s\n"%(val[0], val[1]))

def plot(file):
    with open(file, 'rb') as f:
            plist = plistlib.load(f)
    tracks = plist['Tracks']
    print(tracks)
    ratings = []
    time = []
    for trackID, track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            time.append(track['Total Time'])

        except:
            pass
    if ratings == [] or time == []:
        print("Invalid input.")
        return

    x = np.array(time, np.int32)
    x = x/60000.0
    y = np.array(ratings, np.int32)
    plt.subplot(2, 1, 1)
    plt.plot(x, y, 'o')
    plt.axis([0, 1.05*np.max(x), -1, 110])
    plt.xlabel('Track Duration')
    plt.ylabel('Rating')

    plt.subplot(2, 1, 2)
    plt.hist(x, bins=20)
    plt.xlabel('Track Duration')
    plt.ylabel('Count')
    plt.show()

def findCommon(files):
    tracknamesets = []
    for file in files:
        tracknames = set()
        with open(file, 'rb') as f:
            plist = plistlib.load(f)
        tracks = plist['Tracks']
        for trackID, track in tracks.items():
            try:
                tracknames.add(track['Name'])
            except:
                pass
        tracknamesets.append(tracknames)

    common = set.intersection(*tracknamesets)
    if len(common) > 0:
        with open('common.txt', 'w') as f:
            for val in common:
                s = "%s"%val
                f.write(str(s.encode("UTF-8"))[1:]+"\n")
        print("Common Tracks Found. Track Names written to common.txt.")

    else:
        print("No Common Tracks.")

def main():
    desc = """Analysing Itunes playlists from XML(.xml) files."""
    parser = arg.ArgumentParser(description=desc)
    group = parser.add_mutually_exclusive_group()

    group.add_argument("--common", nargs="*", dest="plFiles", required=False)
    group.add_argument("--stats", dest="plFile", required=False)
    group.add_argument("--dup", dest='plFileD', required=False)

    args = parser.parse_args()

    if args.plFiles:
        findCommon(args.plFiles)
        print("Enter")
    elif args.plFile:
        plot(args.plFile)
    elif args.plFileD:
        find_duplicates(args.plFileD)
    else:
        print("Try again.")

if __name__ == "__main__":
    main()