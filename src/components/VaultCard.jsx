function VaultCard({ item }) {
  return (
    <div className="bg-gray-900 p-6 rounded-xl shadow-lg">
      <h3 className="text-lg font-bold text-purple-400">
        {item.category}
      </h3>

      <p className="mt-2 text-gray-300">
        {item.summary}
      </p>

      <p className="mt-4 text-xs text-gray-500 break-all">
        Hash: {item.hash}
      </p>
    </div>
  );
}

export default VaultCard;