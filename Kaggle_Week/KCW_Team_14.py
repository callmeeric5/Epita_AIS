import os
import random
from typing import Set, List
from tqdm import tqdm
import argparse


class Pating:
    def __init__(self, line, idx):
        infos = line.split()
        self.idx = idx
        self.type = infos[0]
        self.tags = set(infos[2:])

    def __repr__(self):
        return f"Pating(index={self.idx}, type={self.type}, tags={self.tags})"


class FrameGlass:
    def __init__(self, tags: Set[str], idx: str):
        self.tags = tags
        self.idx = idx

    def __repr__(self):
        return f"FrameGlass(id={self.idx}, tags={self.tags})"


class PortraitFG(FrameGlass):
    def __init__(self, portrait1, portrait2):
        super().__init__(
            tags=portrait1.tags.union(portrait2.tags),
            idx=f"{portrait1.idx}P{portrait2.idx}",
        )


class LandscapeFG(FrameGlass):
    def __init__(self, landscape):
        super().__init__(tags=landscape.tags, idx=f"{landscape.idx}L")


class Scorer:

    def __init__(self, input_file, sub_file):

        self.frameglasses = {}
        self.usedframeglasses = {}
        self.sub = open(sub_file, "r")
        self.actual_frameglass = []
        self.prev_frameglass = []
        self.score = 0
        self.debug = False

        f = open(input_file, "r")
        for count, i in enumerate(f.readlines()[1:]):
            self.frameglasses[count] = i.split()
            self.usedframeglasses[count] = False

    def frameglass_checking(self, frameglass_elements):

        if len(frameglass_elements) == 1:
            if self.frameglasses[int(frameglass_elements[0])][0] == "L":
                if self.usedframeglasses[int(frameglass_elements[0])] == True:
                    raise Exception(
                        "Error:",
                        "Multiple use of frameglasses " + frameglass_elements[0],
                    )
                tags = self.frameglasses[int(frameglass_elements[0])][2:]
                self.usedframeglasses[int(frameglass_elements[0])] = True
                return tags
            else:
                raise Exception("Error:", "THE TYPE OF PAINTING")
        elif len(frameglass_elements) == 2:
            if (
                self.frameglasses[int(frameglass_elements[0])][0] == "P"
                and self.frameglasses[int(frameglass_elements[1])][0] == "P"
            ):
                if self.usedframeglasses[int(frameglass_elements[0])] == True:
                    raise Exception(
                        "Error:",
                        "Multiple use of frameglasses " + frameglass_elements[0],
                    )
                if self.usedframeglasses[int(frameglass_elements[1])] == True:
                    raise Exception(
                        "Error:",
                        "Multiple use of frameglasses " + frameglass_elements[1],
                    )
                tags = list(
                    set(
                        self.frameglasses[int(frameglass_elements[0])][2:]
                        + self.frameglasses[int(frameglass_elements[1])][2:]
                    )
                )
                self.usedframeglasses[int(frameglass_elements[0])] = True
                self.usedframeglasses[int(frameglass_elements[1])] = True
                return tags
            else:
                raise Exception("Error:", "THE TYPE OF PAINTING")
        else:
            raise Exception("Error:", "THE TYPE OF PAINTING")

    def exhibition_walk(self):

        for frame in self.sub.readlines()[1:]:

            self.actual_frameglass = self.frameglass_checking(frame.strip().split())
            if self.prev_frameglass != []:
                self.scorer(self.actual_frameglass, self.prev_frameglass)
            self.prev_frameglass = self.actual_frameglass

    def scorer(self, frame1, frame2):

        intersection = list(set(frame1).intersection(frame2))
        val1 = len(intersection)
        val2 = len(frame1) - len(intersection)
        val3 = len(frame2) - len(intersection)
        self.score += min(val1, val2, val3)


def create_frame_glasses(patings: List[Pating], batch_size=1000) -> List[FrameGlass]:
    landscape_frames = [LandscapeFG(p) for p in patings if p.type == "L"]
    portraits = [p for p in patings if p.type == "P"]
    portrait_frames = []
    portrait_tags = {portrait: portrait.tags for portrait in portraits}
    used_indices = set()
    with tqdm(total=len(portraits), desc="Processing portraits") as progress_bar:
        for i in range(0, len(portraits), batch_size):
            batch = portraits[i : i + batch_size]
            for portrait in batch:
                if portrait.idx in used_indices:
                    continue
                best_pair = None
                max_difference = -1
                for other_portrait in batch:
                    if other_portrait == portrait or other_portrait.idx in used_indices:
                        continue
                    difference = len(
                        portrait_tags[portrait].symmetric_difference(
                            portrait_tags[other_portrait]
                        )
                    )
                    if difference > max_difference:
                        max_difference = difference
                        best_pair = other_portrait
                if best_pair:
                    portrait_frames.append(PortraitFG(portrait, best_pair))
                    used_indices.update([portrait.idx, best_pair.idx])
                    progress_bar.update(1)
    frame_glasses = landscape_frames + portrait_frames
    frame_glasses.sort(key=lambda fg: len(fg.tags))
    return frame_glasses


def calculate_satisfaction(fg1: FrameGlass, fg2: FrameGlass) -> int:
    return min(
        len(fg1.tags - fg2.tags), len(fg1.tags & fg2.tags), len(fg2.tags - fg1.tags)
    )


def arrange_frame_glasses(
    frame_glasses: List[FrameGlass], sample_size=3000
) -> List[FrameGlass]:
    arranged = [frame_glasses.pop(0)]
    progress_bar = tqdm(total=len(frame_glasses) + 1, desc="Arranging frameglasses")
    progress_bar.update(1)

    while frame_glasses:
        if len(frame_glasses) > sample_size:
            sample = random.sample(frame_glasses, sample_size)
        else:
            sample = frame_glasses
        next_frame = max(
            sample, key=lambda fg: calculate_satisfaction(arranged[-1], fg)
        )
        frame_glasses.remove(next_frame)
        arranged.append(next_frame)
        progress_bar.update(1)
    progress_bar.close()
    return arranged


def load_patings(file):
    patings = []
    with open(file) as f:
        line = f.readline()
        line = f.readline()
        idx = 0
        while line:
            patings.append(Pating(line, idx))
            idx += 1
            line = f.readline()
    return patings


def save_files(frame_glasses, file):
    with open(file, "w") as f:
        f.write(str(len(frame_glasses)) + "\n")
        for fg in frame_glasses:
            line = fg.idx.replace("L", "").replace("P", " ") + "\n"
            f.write(line)


def main(input_folder="KaggleData", output_folder="Test"):
    input_files = os.listdir(input_folder)
    total_score = 0
    for input_file in input_files:
        input_path = os.path.join(input_folder, input_file)
        patings = load_patings(input_path)
        frame_glasses = create_frame_glasses(patings, batch_size=10)  # Only for testing
        sorted_frame_glasses = arrange_frame_glasses(
            frame_glasses, sample_size=10
        )  # Only for testing

        output_file = os.path.join(output_folder, input_file)
        save_files(sorted_frame_glasses, output_file)
        score = Scorer(input_path, output_file)
        score.exhibition_walk()
        total_score += score.score
        print(f"Final score for {input_file} = {score.score}")
        print("*" * 80)

    print("-" * 80)
    print(f"Total score = {total_score}")


if __name__ == "__main__":
    main()
