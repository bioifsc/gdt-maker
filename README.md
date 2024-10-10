# gdt-maker
GDT-Maker - Genome Distance Tree Maker

# How to run

## Create a docker image

```
git clone https://github.com/bioifsc/gdt-maker.git
cd gdt-maker/
docker build -t bioifsc/gdt-maker .
```

## Run

```
docker run -it --rm -v ${PWD}:/data bioifsc/gdt-maker gdt.py -h
```
