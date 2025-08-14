import { useState, useEffect } from "react";
import React from "react";

const SupportTicketForm = ({ ticket, onSave, onCancel, customers }) => {
  const [formData, setFormData] = useState(
    ticket || {
      customerId: "",
      subject: "",
      description: "",
      status: "open",
      priority: "medium",
      assignedTo: "",
      resolution: "",
    }
  );

  useEffect(() => {
    if (ticket) {
      setFormData(ticket);
    } else if (customers.length > 0 && !formData.customerId) {
      setFormData((prevData) => ({
        ...prevData,
        customerId: customers[0].id, // Default to the first customer
      }));
    }
  }, [ticket, customers, formData.customerId]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  // Add your component JSX here
  return (
    <div className="bg-white p-6 rounded-lg shadow-lg max-w-lg mx-auto mt-8">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">
        {ticket ? "Edit Support Ticket" : "Create Support Ticket"}
      </h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-gray-700 mb-2" htmlFor="customerId">
            Customer
          </label>
          <select
            id="customerId"
            name="customerId"
            value={formData.customerId}
            onChange={handleChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            required
            disabled={!!!ticket} // disable if editing an existing ticket
          >
            <option value="">Select a customer</option>
            {customers.map((customer) => (
              <option key={customer.id} value={customer.id}>
                {customer.name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label
            htmlFor="subject"
            className="block text-sm font-medium text-gray-700"
          >
            Subject
          </label>
          <input
            type="text"
            id="subject"
            name="subject"
            value={formData.subject}
            onChange={handleChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            required
          />
        </div>
        <div>
          <label
            className="block text-sm font-medium text-gray-700"
            htmlFor="description"
          >
            Description
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows={5}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            required
          ></textarea>
        </div>
        <div>
          <label
            className="block text-sm font-medium text-gray-700"
            htmlFor="status"
          >
            Status
          </label>
          <select
            id="status"
            name="status"
            value={formData.status}
            onChange={handleChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          >
            <option value="open">Open</option>
            <option value="in_progress">In Progress</option>
            <option value="resolved">Resolved</option>
            <option value="on_hold">On Hold</option>
            <option value="closed">Closed</option>
          </select>
        </div>
        <div>
          <label
            className="block text-sm font-medium text-gray-700"
            htmlFor="priority"
          >
            Priority
          </label>
          <select
            id="priority"
            name="priority"
            value={formData.priority}
            onChange={handleChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="urgent">Urgent</option>
          </select>
        </div>
        <div>
          <label
            className="block text-sm font-medium text-gray-700"
            htmlFor="assignedTo"
          >
            Assigned To
          </label>
          <input
            type="text"
            id="assignedTo"
            name="assignedTo"
            value={formData.assignedTo}
            onChange={handleChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
        </div>
        {formData.status === "resolved" || formData.status === "closed" ? (
          <>
            <div className="">
              <label
                className="block text-sm font-medium text-gray-700"
                htmlFor="resolution"
              >
                Resolution
              </label>
              <textarea
                id="resolution"
                name="resolution"
                value={formData.resolution}
                onChange={handleChange}
                rows={3}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              ></textarea>
            </div>
          </>
        ) : null}
        <div className="flex justify-end space-x-3 mt-6">
          <button
            type="button"
            className="bg-blue-500 text-white px-4 py-2 rounded-lg"
          >
            onClick = {onCancel}
            Cancel
          </button>
          <button
            type="submit"
            onClick={onSubmit}
            className="px-4 py-2 bg-gray-300 text-gray-800 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition duration-150 ease-in-out"
          >
            Submit Ticket
          </button>
        </div>
      </form>
    </div>
  );
};
