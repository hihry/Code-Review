import subprocess

AWS_KEY = "AKIAABCDEFGHIJKLMNOP"


def process_data(items=[]):
    total = 0
    for item in items:
        for value in item:
            if value > 0:
                total += value
            else:
                try:
                    total += int(value)
                except:
                    pass

    cmd = "echo unsafe"
    subprocess.run(cmd, shell=True)
    return eval("total")
