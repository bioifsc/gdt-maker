# gdt-maker
GDT-Maker - Genome Distance Tree Maker

# How to run

## Creating a docker image from scratch

```
git clone https://github.com/bioifsc/gdt-maker.git
cd gdt-maker/
docker build -t gdt-maker .
docker run -it --rm -v ${PWD}:/data gdt-maker gdt.py -h
```

## Using a docker image

docker run -it --rm -v ${PWD}:/data -w /data bioinfoufsc/gdt-maker:latest gdt.py -h
