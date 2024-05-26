import torch
import torch.nn as nn
from einops.layers.torch import Rearrange


class Net(nn.Module):
    def __init__(self, upscale_factor):
        super(Net, self).__init__()

        # DESIGN YOUR MODEL ARCHITECTURE HERE

        self.block1 = nn.Sequential(
            nn.Conv2d(1, 128, kernel_size=5, padding=2),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
        )

        self.block2 = nn.Sequential(
            nn.Conv2d(128, 64, kernel_size=5, padding=2),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
        )

        self.block3 = nn.Sequential(
            nn.Conv2d(64, 64 * (upscale_factor**2), kernel_size=3, padding=1),
            # nn.PixelShuffle(upscale_factor),
            Rearrange(
                "b (c uf1 uf2) h w -> b c (h uf1) (w uf2)",
                uf1=upscale_factor,
                uf2=upscale_factor,
            ),  # Use einops instead of PixelShuffle
            nn.ReLU(),
            nn.Conv2d(64, 1, kernel_size=3, padding=1),
        )

    def forward(self, x):
        # RUN YOUR MODEL ARCHITECTURE HERE

        x = self.block1(x)
        x = self.block2(x)
        x = self.block3(x)
        return x
