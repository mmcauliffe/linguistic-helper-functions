form Variables
                      sentence filename
                    endform

                    Read from file... 'filename$'
                    To Intensity... 100 0.001 yes

                    frames = Get number of frames

                    output$ = "time(s)"+tab$+"Intensity(dB)"+newline$

                    for f from 1 to frames
                        t = Get time from frame number... 'f'
                        t$ = fixed$(t, 3)
                        v = Get value in frame... 'f'
                        v$ = fixed$(v, 2)
                        output$ = output$+t$+tab$+v$+newline$
                    endfor

                    echo 'output$'