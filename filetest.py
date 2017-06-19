with open('map.html', 'r') as f_in:
    with open('file2.txt','w') as f_out:
        for line_no, line in enumerate(f_in, 1):
            if line_no == 10:
                f_out.write('Hello at line 10\n')
            f_out.write(line)