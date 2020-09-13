# Gaze on Grid

An eye-tracking project based on [GazeCloudAPI](https://gazerecorder.com/gazecloudapi/).

# Component

## Image Crawling

dir: `image-crawler`

Images are downloaded from [Zalando Germany](zalando.de) by Scrapy.

## Eye Tracking

dir: `experiment-interface`

Eye tracking is conducted by web and [GazeCloudAPI](https://gazerecorder.com/gazecloudapi/).

## Data Analysis

dir `data-analysis`

Identify Fixation based on IVT alogrithm; generate images with fixation points and scan path.