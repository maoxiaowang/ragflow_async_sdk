================================
RAGFlow Async SDK Documentation
================================

The RAGFlow Async SDK provides a Pythonic, asynchronous interface to interact with RAGFlow services.
All operations are designed to be asynchronous and easy to integrate into modern Python workflows.

Quick Start
===========

💿 **Installation**

Requires Python 3.10+.

.. code-block:: bash

    pip install ragflow-async-sdk

🚀 **Getting Started**

All operations in the RAGFlow Async SDK are asynchronous. To use the SDK, first initialize the client and then run async calls inside Python's `asyncio` event loop.

🛠 **Initialization**

.. code-block:: python

    from ragflow_async_sdk import AsyncRAGFlowClient

    client = AsyncRAGFlowClient(
        server_url="http://your-ragflow-address",
        api_key="YOUR_API_KEY",
    )

⏩ **Run with asyncio**

.. code-block:: python

    import asyncio

    async def main():
        # Example: Health check
        system_health = await client.systems.healthz()
        print(system_health.status)

    # Run the async main function
    asyncio.run(main())

Quick Links
===========

.. toctree::
   :maxdepth: 2

   sphinx/client
   sphinx/modules
   sphinx/models
   sphinx/types
   sphinx/errors
   sphinx/compatibility