# CS 201 Data Structures II, Spring 2021
# Final Project: Footprint Calculator
# Group Members:
- _Muhammad Ammar Khan_
- _Ahsan Ali_
- _Wasiq Hussain_
- _Aliza Rafique_
-------

The final project for this course required the implementation of the assigned data structure using the application.

## Youtube Demo Link

https://www.youtube.com/watch?v=9tnrmx0ZU5g

## Background

Greenhouse emission is one of the major crises the world is facing at the moment caused by factors ranging from automotive, industrial machinery to agricultural practices. Therefore, an urgent demand for the solution has risen. With this application, we intend to help the user identify the footprint consumption for their products and minimize it. 

## ScapeGoat Trees

Scapegoat trees are self-balancing binary search trees. The main idea of the structure is based on the concept of a scapegoat. A scapegoat is defined as someone who is blamed for the wrongdoings of others. Few insert and delete operations can make the tree unbalanced and to rebalance the tree, a scapegoat, a node, is searched. When the scapegoat is found the entire subtree rooted at the scapegoat can be rebuilt at zero cost, in an amortized sense. Scapegoat trees have O(log n) worst-case search time without storing any extra information like red-black trees. 

## Application

The application will provide the spot footprint calculator to allow the user to capture an image using the cellphone camera and hit the compute button to let our algorithm perform carbon and water footprint analysis which will tell the user how sustainable and environmental friendly using a footprint health progress bar to make the output interactive. The application was designed using an image detection method using OCR to detect items and ingredients within food products to estimate carbon and water footprint. These detected foods are searched in the created scapegoat data structure to extract the parameters for rainwater, agricultural feed, and underground water for water footprint. And similarly carbon dioxide, sulfur dioxide, and Phosphorous oxide emission for the Carbon footprint.

## Application Usage

- About: Details usage and purpose of application
- Calculate: Lead user to the calculator

- Upload Image: Loads image into the program
- Reset: Clear all entries
- Add Item: Add additional ingredient to detected items
- Compute: Compute the footprint for the given food

## OCR Implementation

Since the application consists of optical character recognition, it was necessary to perform certain image operations on images captured from the backside of the food products to get optimized results in the tesseract library built-in functions for OCR. Therefore, the image was processed with resizing, filtering, binarization, and contrast which yielded a better image compared to the raw one, and therefore, the OCR was able to perform much better on this processed image. The comparison of raw (left) and processed image (right) can be seen below.


![alt text](https://github.com/WasiqMemon/dummy-documents/blob/main/comparision.png)


## Libraries Used
- Tesseract
- Matplotlib
- CV2
- Pillow
- Numpy
- Pandas
- Tkinter


## References for Dataset Used

- https://science.sciencemag.org/content/suppl/2018/05/30/360.6392.987.DC1
- https://www.kaggle.com/selfvivek/environment-impact-of-food-production
- https://resourcewatch.org/data/explore/Foo_046-Food-Footprint-in-Calories
- https://www.programiz.com

## Reference to Data Structure Used

- https://github.com/satchamo/Scapegoat-Tree
