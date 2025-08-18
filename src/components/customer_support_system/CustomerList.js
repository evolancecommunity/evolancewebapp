import React, { useState, useEffect, useContext } from "react";
import { AuthContext } from "../../App";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const CustomerList = ({customers, onEdit, onDelete, onViewInteractions}) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-lg max-w-4xl mx-auto mt-8">
        <h2 className="text-2xl font-bold mb-6 text-gray-800">Customer List</h2>
        {customers.length === 0 ? (
          <p className="text-gray-600">No customers found. Add a new customer.</p>
        ):(
         <div className="overflow-x-auto">   
            <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                <tr>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Company</th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                {customers.map((customer) => (
                    <tr key={customer.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{customer.name}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{customer.email}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{customer.company || 'N/A'}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex items-center space-x-3">
                        <button onClick={() => onEdit(customer)} className="text-blue-600 hover:text-blue-900 transition duration-150 ease-in-out" title="Edit Customer"><Edit className="h-5 w-5" /></button>
                        <button onClick={() => onDelete(customer.id)} className="text-red-600 hover:text-red-900 transition duration-150 ease-in-out" title="Delete Customer"><Trash className="h-5 w-5" /></button>
                        <button onClick={() => onViewInteractions(customer.id)} className="text-green-600 hover:text-green-900 transition duration-150 ease-in-out" title="View Customer Interactions"><View className="h-5 w-5" /></button>
                      </div>
                    </td>
                    </tr>
                ))}
                </tbody>
            </table>
          </div>
        )}
    </div>
    
  )

}

export default CustomerList;