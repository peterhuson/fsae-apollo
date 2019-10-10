from multiprocessing import Process


def runDataReceiving():
    pass


def runDisplay():
    pass


def runSteeringWheel():
    # create process for display and data reception
    dataReceiving = Process(target=runDataReceiving())
    display = Process(target=runDisplay)

    dataReceiving.start()
    display.start()
    
    # don't finish while dataReceiving and display are running
    dataReceiving.join()
    display.join()


if __name__ == "__main__":
    runSteeringWheel()
