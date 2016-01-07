Commands for retrieving share URLs for files uploaded to Dropbox:

    $ find . -type f | sort | cut -d '/' -f 2- | tee files.txt
    $ cat files.txt | tr "\n" "\0" | xargs -0 -I{} dropbox_uploader.sh share "/TRB ADC70/doc/{}" | tee urls.txt
