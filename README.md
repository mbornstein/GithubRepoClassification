# Github Repository Classification
classifies Github repos - more to come


## Requirements
* Python3
* Git must be installed and in system path

## Categories

* DEV​ – a repository primarily used for development of a tool, component, application, app, or
API
* HW​ repo – a repository primarily used for homework, assignments and other course-related
work and code
* EDU​ – a repository primarily used to host tutorials, lectures, educational information and
code related to teaching
* DOCS​ – a repository primarily used for tracking and storage of non-educational documents
* WEB​ - a repository primarily used to host static personal websites or blogs
* DATA​ - a repository primarily used to store data sets
* OTHER​ – use this category only if there is no strong correlation to any other repository
category, for example, empty repositories

## Metrics

### Repository size
The repository size in bytes (kb???).
All repositories of size zero  are in the category OTHER.
Repositories of each category can have a small size but we only expect DEV, DOCS, DATA and WEB repository to have a big size.

### Watcher count
The watcher count indicates the popularity of a repository.
We expect only DEV repositories to have a watcher count.
EDU could also have an higher than average watcher count.

### Forks count
Similar to watcher count, but only DEV repositories.

### Open issues
Popularity indication. Mostly for DEV.

### Up-to-dateness
How recent is the last commit?
Repositories that are continuously worked on have a high up-to-dateness (DEV, DOCS).
We expect that repositories from other categories are inacive after some time and have low up-to-dateness.

### File count
We have no assumptions how the categories influence the file count.

### File folder ratio
Many Directories for DOCS and partly DEV (java programs).

### Average folder depth
Same as File folder ratio.

### Average entropy
High for DATA and EDU (pictures, videos, text)
Medium for DOCS, WEB (Text, some pictures)
Low for DEV, HW (code)

## Metrics not implemented yet

### Average File Size
Big size: DATA
Small size: DEV, rest


## Problems with kmeans
* All metrics are equally important
* Cannot learn dependencies between metrics

## Null accuracy
Around 75% if we only guess DEV.
Idea: Classify DEV vs non-DEV. And a second stage to classify the rest if it is no DEV.

## TODO
* Two stage classification (DEV/not DEV)
* moar metrics
* visualize metric distribution (each metric/ color coding)
* visualize boxplot per category per metric
* Tips with to do if high null accuracy
