import ptvsd
ptvsd.enable_attach(("0.0.0.0", 3000))
print("Waiting")
ptvsd.wait_for_attach()
print("Connected")
print ("ptvsd version is: " + ptvsd.__version__)
input('Press Enter to Exit')