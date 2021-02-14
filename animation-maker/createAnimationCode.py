if __name__ == '__main__':

    fileName = input('input file name:')

    f = open(fileName, 'r')
    fl = f.readlines()
    f.close()

    # remove newline
    for i in range(len(fl)):
        fl[i] = fl[i].replace('\n', '')

    # width, height and divide
    info = fl[0].split(' ')
    
    width = info[0].split('=')[1]
    height = info[1].split('=')[1]
    divide = info[2].split('=')[1]

    # write to each file
    animationXmls = []
    animationFileNames = []
    pathNames = []
    colors = []
    
    drawableVectorXml = ('<?xml version="1.0" encoding="utf-8"?>\n' +
                         '<vector xmlns:android="http://schemas.android.com/apk/res/android"\n' +
                         '\tandroid:width="' + str(width) + 'dp"\n' +
                         '\tandroid:height="' + str(height) + 'dp"\n' +
                         '\tandroid:viewportWidth="' + str(float(width)/float(divide)) + '"\n' +
                         '\tandroid:viewportHeight="' + str(float(height)/float(divide)) + '">\n\n')
                         
    drawableAnimatedVectorXml = ('<?xml version="1.0" encoding="utf-8"?>\n' +
                                 '<animated-vector\n' +
                                 '\txmlns:android="http://schemas.android.com/apk/res/android"\n' +
                                 '\tandroid:drawable="@drawable/anim_test">\n\n')

    resStringsXml = ''

    # write for each item
    lineCount = 1

    thisPaths = []
    
    while True:

        while True:

            # animation file name
            if fl[lineCount] == 'animation_file_name':
                thisAnimationFileName =  fl[lineCount + 1]
                animationFileNames.append(thisAnimationFileName)

            # path_name
            elif fl[lineCount] == 'path_name':
                thisPathName = fl[lineCount + 1]
                pathNames.append(thisPathName)

            # color
            elif fl[lineCount] == 'color':
                thisColor = fl[lineCount + 1]
                colors.append(thisColor)

            # path
            elif fl[lineCount] == 'path':

                while fl[lineCount + 1] != 'time' and fl[lineCount + 1] != '':
                    this_path = fl[lineCount + 1].split(' ')
                    this_pathCode = ''

                    for i in range(len(this_path)):
                        this_subpath = this_path[i]

                        # line
                        if len(this_subpath.split('-')) == 1:
                            
                            this_subpath_x = this_subpath.split(',')[0]
                            this_subpath_y = this_subpath.split(',')[1]
                            
                            if i == 0:
                                this_pathCode += ('M' + str(float(this_subpath_x) / float(divide)) +
                                                  ',' + str(float(this_subpath_y) / float(divide)) + ' ')
                            else:
                                this_pathCode += ('L' + str(float(this_subpath_x) / float(divide)) +
                                                  ',' + str(float(this_subpath_y) / float(divide)) + ' ')

                        # curve
                        elif len(this_subpath.split('-')) == 3:

                            this_subpath_mid0 = this_subpath.split('-')[0]
                            this_subpath_mid1 = this_subpath.split('-')[1]
                            this_subpath_dest = this_subpath.split('-')[2]

                            this_subpath_mid0_x = this_subpath_mid0.split(',')[0]
                            this_subpath_mid0_y = this_subpath_mid0.split(',')[1]

                            this_subpath_mid1_x = this_subpath_mid1.split(',')[0]
                            this_subpath_mid1_y = this_subpath_mid1.split(',')[1]

                            this_subpath_dest_x = this_subpath_dest.split(',')[0]
                            this_subpath_dest_y = this_subpath_dest.split(',')[1]

                            this_pathCode += ('C' + str(float(this_subpath_mid0_x) / float(divide)) +
                                              ',' + str(float(this_subpath_mid0_y) / float(divide)) +
                                              ' ' + str(float(this_subpath_mid1_x) / float(divide)) +
                                              ',' + str(float(this_subpath_mid1_y) / float(divide)) +
                                              ' ' + str(float(this_subpath_dest_x) / float(divide)) +
                                              ',' + str(float(this_subpath_dest_y) / float(divide)) + ' ')

                    lineCount += 1

                    thisPaths.append(this_pathCode)

            # time
            elif fl[lineCount] == 'time':
                this_times = fl[lineCount + 1].split(',')

            # check if end of animation item
            lastLineOfThisItem = False
            if lineCount + 1 >= len(fl):
                lastLineOfThisItem = True
            elif fl[lineCount + 1] == 'animation_file_name':
                lastLineOfThisItem = True

            # write if end of animation item
            if lineCount > 2 and lastLineOfThisItem == True:

                # this animationXml
                thisAnimationXml = ('<?xml version="1.0" encoding="utf-8"?>\n' +
                                    '<set xmlns:android="http://schemas.android.com/apk/res/android"\n' +
                                    'xmlns:aapt="http://schemas.android.com/aapt">\n\n')
                
                for i in range(len(this_times)-1):
                    thisAnimationXml += ('\t<objectAnimator\n' +
                                         '\t\tandroid:propertyName="pathData"\n' +
                                         '\t\tandroid:duration="' + str(int(this_times[i + 1]) - int(this_times[i])) + '"\n' +
                                         '\t\tandroid:startOffset="' + str(int(this_times[i])) + '"\n' +
                                         '\t\tandroid:valueFrom="@string/' + thisPathName + '_' + str(i) + '"\n' +
                                         '\t\tandroid:valueTo="@string/' + thisPathName + '_' + str(i + 1) + '"\n' +
                                         '\t\tandroid:valueType="pathType" />\n')

                thisAnimationXml += '</set>'

                # drawableVectorXml
                drawableVectorXml += ('\t<group>\n' +
                                      '\t\t<path\n' +
                                      '\t\t\tandroid:name="' + thisPathName + '"\n' +
                                      '\t\t\tandroid:pathData="@string/' + thisPathName + '_0"\n' +
                                      '\t\t\tandroid:fillColor="#' + thisColor + '"/>\n' +
                                      '\t</group>\n')

                # drawableAnimatedVectorXml
                drawableAnimatedVectorXml += ('\t<target android:name="' + thisPathName +
                                              '" android:animation="@anim/' + thisAnimationFileName[:len(thisAnimationFileName)-4] + '"/>\n')
                # resStringsXml
                for i in range(len(this_times)):
                    resStringsXml += ('\t<string name="' + thisPathName + '_' + str(i) + '">' + thisPaths[i] + '</string>\n')

                animationXmls.append(thisAnimationXml)

                thisPaths = []

                lineCount += 1
                
                break

            lineCount += 1

        if lineCount >= len(fl):
            break

    # suffix for each file
    drawableVectorXml += '</vector>'

    drawableAnimatedVectorXml += '</animated-vector>'

    # write final code to file
    f = open('finalCode.txt', 'w')
    finalCode = ''
    
    for i in range(len(animationFileNames)):
        finalCode += '\n\n\n### insert below into res/anim/' + str(animationFileNames[i]) + ' ###\n'
        finalCode += animationXmls[i]

    finalCode += '\n\n\n### insert below into res/drawable/anim_test.xml ###\n'
    finalCode += drawableVectorXml

    finalCode += '\n\n\n### insert below into res/drawable/XXX.xml where app:srcCompat attribute of ImageView is "@drawable/XXX" ###\n'
    finalCode += drawableAnimatedVectorXml

    finalCode += '\n\n\n### add below into strings.xml ###\n'
    finalCode += resStringsXml

    f.write(finalCode)
    f.close()
