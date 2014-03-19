
form Variables
    sentence firstfile
    sentence secondfile
    real maxFreq
endform

Read from file... 'firstfile$'
first = selected()

Read from file... 'secondfile$'
second = selected()

select first
To Spectrogram... 0.005 maxFreq 0.002 20 Gaussian
first_spec = selected()

select second
To Spectrogram... 0.005 maxFreq 0.002 20 Gaussian
second_spec = selected()

select first_spec
plus second_spec
To DTW... 1 1 no restriction
spec_dist = Get distance (weighted)

echo 'spec_dist'