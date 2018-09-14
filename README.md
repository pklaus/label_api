# label\_api

Install requirements:

    pip install -r requirements.txt

Run:

    ./label_api --help
    # for example:
    ./label_api --port 8080 --model QL-800 --printer usb://0x04f9:0x2015 --backend pyusb

The CLI signature of `label_api` is as follows:

    Usage: label_api [OPTIONS]
    
      Start the label_api software
    
    Options:
      --host TEXT     Host / IP to listen on
      --port INTEGER  Port to listen on
      --model TEXT    brother_ql model
      --backend TEXT  brother_ql backend
      --printer TEXT  brother_ql printer
      --debug         Enable verbose debugging output
      --help          Show this message and exit.
