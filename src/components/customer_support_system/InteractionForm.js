import {useState} from "react";

const InteractionForm = ({ customerId, interaction, onSave, onCancel }) => {

    const [formData, setFormData] = useState(interaction || {
        customer_id: customerId,
        type: "chat",
        date: new Date().toISOString().split("T")[0],
        summary: "",
    });

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

    return (
        <div className="bg-white p-6 rounded-lg shadow-lg max-w-lg mx-auto mt-8">
            <h2 className="text-2xl font-bold mb-6 text-gray-800">
                {interaction ? "Edit Interaction" : "Add New Interaction"}
            </h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="type" className="block text-sm font-medium text-gray-700">Type</label>
                    <select
                        type="text"
                        name="type"
                        value={formData.type}
                        onChange={handleChange}
                        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                        required
                    >
                        <option value="chat">Chat</option>
                        <option value="email">Email</option>
                        <option value="meeting">Phone</option>
                    </select>
                </div>
                <div>
                    <label htmlFor="summary" className="block text-sm font-medium text-gray-700">Summary</label>
                    <textarea
                        id="summary"
                        name="summary"
                        value={formData.summary}
                        onChange={handleChange}
                        rows="4"
                        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                        required
                    ></textarea>
                </div>
                <div className="flex justify-end space-x-3 mt-6">
                    <button type="submit" className="px-4 py-2 bg-gray-300 text-gray-800 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition duration-150 ease-in-out">
                        Save
                    </button>
                    <button type="button" onClick={onCancel} className="px-4 py-2 bg-gray-300 text-gray-800 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition duration-150 ease-in-out">
                        Cancel
                    </button>
                </div>
            </form>
        </div>
    );

};

export default InteractionForm;
