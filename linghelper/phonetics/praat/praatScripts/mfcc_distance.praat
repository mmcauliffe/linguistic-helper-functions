form Variables
                                            sentence firstfile
                                            sentence secondfile
                                            real maxMel
                                        endform

                                        Read from file... 'firstfile$'
                                        first = selected()

                                        Read from file... 'secondfile$'
                                        second = selected()

                                        select first
                                        To MFCC... 20 0.015 0.005 100.0 100.0 0.0
                                        first_mfcc = selected()

                                        select second
                                        To MFCC... 20 0.015 0.005 100.0 100.0 0.0
                                        second_mfcc = selected()


                                        select first_mfcc
                                        plus second_mfcc
                                        To DTW... 1.0 0.0 0.0 0.0 0.056 1 1 no restriction
                                        mfcc_dist = Get distance (weighted)

                                        echo 'mfcc_dist'