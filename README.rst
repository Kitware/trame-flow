Trame Flow
----------------------------------------

A node editor for `trame <https://kitware.github.io/trame/>`_ based on `VueFlow <https://vueflow.dev/>`_.

.. image:: screenshot.png

License
----------------------------------------

This library is OpenSource and follow the MIT License.

Installation
----------------------------------------

Install the application/library.

.. code-block:: console

    pip install trame-flow

Usage
-----

Examples can be found in the examples directory. To run them you need trame and trame-vuetify.

Development setup
----------------------------------------

We recommend using uv for setting up and managing a virtual environment for your development.

.. code-block:: console

    # Create venv and install all dependencies
    uv sync --all-extras --dev

    # Activate environment
    source .venv/bin/activate

    # Install commit analysis
    pre-commit install
    pre-commit install --hook-type commit-msg

    # Allow live code edit
    uv pip install -e .


Build and install the Vue components.

.. code-block:: console

    cd vue-components
    npm i
    npm run build
    cd -

For running tests and checks, you can run ``nox``.

.. code-block:: console

    # run all
    nox

    # lint
    nox -s lint

    # tests
    nox -s tests

Professional Support
----------------------------------------

* `Training <https://www.kitware.com/courses/trame/>`_: Learn how to confidently use trame from the expert developers at Kitware.
* `Support <https://www.kitware.com/trame/support/>`_: Our experts can assist your team as you build your web application and establish in-house expertise.
* `Custom Development <https://www.kitware.com/trame/support/>`_: Leverage Kitware’s 25+ years of experience to quickly build your web application.
