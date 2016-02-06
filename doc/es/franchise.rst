***********
Franquicias
***********

Las franquicias sirven, principalmente, para identificar las ventas que se le
hacen a cada franquicia.

.. inheritref:: sale_franchise/franchise:section:manage_franchises

Gestionar las franquicias
=========================

Des del menú |menu_franchise| podremos dar de alta y modificar los datos de una franquicia.

.. view:: sale_franchise.franchise_view_form
   :field: company_party

   Formulario de una franquicia

Los campos principales que identifican una franquicia son:

* |field_code|
* |field_name|
* |field_company_party|
* |field_address|

El campo |field_company| es opcional, y lo rellenaremos si llevamos la
contabilidad de esta empresa y, por tanto, la tenemos dada de alta en nuestro
sistema.


.. Substitutions

.. |menu_franchise| tryref:: sale_franchise.menu_sale_franchise/complete_name
.. |field_code| field:: sale.franchise/code
.. |field_name| field:: sale.franchise/name
.. |field_company_party| field:: sale.franchise/company_party
.. |field_address| field:: sale.franchise/address
.. |field_company| field:: sale.franchise/company
