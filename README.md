# book_pivot

This repository contains code necessary to create a [Microsoft
Pivot](https://www.microsoft.com/silverlight/pivotviewer/#) collection
of books.

![Screenshot](screenshot.png)

## Demo

Visit [http://books.sortelli.com](http://books.sortelli.com) for a
running demo.

## Building a Colleciton

1) Produce a list of ISBN numbers. One strategy is to use a barcode
reader application on your phone to scan barcodes from books that
you own.

2) Install python packages:

    % pip install -r requirements.txt

3) Put [makedeepzoom](https://github.com/sortelli/makedeepzoom) in
your ```PATH```.

4) Call ```add_book_to_collection.py``` for each ISBN number.
Example:

    % cat isbns.txt | xargs ./add_book_to_collection.py

You can call ```add_book_to_collection.py``` at anytime to add new
books to the collection.

## Serving Content

Serve the following content:

    static-web/
    ├── books.cxml
    ├── collection
    ├── index.html
    └── pivotviewer.xap

Running ```add_book_to_collection.py``` will create the ```collection```
directory and the ```books.cxml``` file. To serve the content,
combine those with ```index.html``` and ```pivotviewer.xap``` and
serve everything as static content.

The application will only work when served through an actually HTTP
server, and will not work if simply loaded in your browser with a
```file://``` URL.

## License

Copyright (c) 2015 Joe Sortelli

MIT License
