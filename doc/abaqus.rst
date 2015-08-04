Abaqus matrices for anisotropic materials
#########################################

:date: 2014-12-17
:tags: Abaqus, anisitropic materials
:author: Roland Smith

Abaqus uses a matrix it calls the D matrix to define the properties of
orthotropic and anisotropic materials.

In the orthotropic case, it takes the following values from the full 6x6
matrix (which I assume is the stiffness or ABD matrix)

    | D1111 D1122 D1133 0     0     0     |
    |       D2222 D2233 0     0     0     |
    |             D3333 0     0     0     |
    |                   D1212 0     0     |
    |       sym.              D1313 0     |
    |                               D2323 |


In the fully anisotropic case, the matrix looks like this:

    | D1111 D1122 D1133 D1112 D1113 D1123 |
    |       D2222 D2233 D2212 D2213 D2223 |
    |             D3333 D3312 D3313 D3323 |
    |                   D1212 D1213 D1223 |
    |       sym.              D1313 D1323 |
    |                               D2323 |

