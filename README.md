HighVolumeAutomationTesting
===========================

High Volume Automation Testing (H-VAT) is a technique that generates many (potentially weak) tests in hopes of finding bugs that standard testing failed to find. It's common for such a technique to generate massive amounts of tests in hopes of finding certain bugs. This implementation attempts to gauge the correctness of audio conversions by using a large audio library and converting a large number of songs. The bugs this project aims to find is somewhat nondeterministic, we assume that the conversion codec works in most cases but that there is a potential edge case where a song loses a noticeable amount of quality.
The software under test is VLC (http://www.videolan.org/).
